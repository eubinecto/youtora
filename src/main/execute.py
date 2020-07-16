import logging
from typing import List

from src.download.downloaders import ChannelDownloader, VideoDownloader
from src.download.models import Video, Caption
from src.query.store import store_channel, store_video, store_caption, store_track

import numpy as np

# for faster video download
# use this later.
from multiprocessing import Process, Manager

from time import sleep


def collect_videos(ns,
                   vid_id_list,
                   lang_code):
    shared_bucket = ns.shared_bucket
    for vid_id in vid_id_list:
        # make a vid_url
        vid_url = "https://www.youtube.com/watch?v={}" \
            .format(vid_id)
        shared_bucket.append(VideoDownloader.dl_video(vid_url=vid_url,
                                                      lang_code=lang_code))
    ns.shared_bucket = shared_bucket


def multiprocess_dl_vids(vid_id_list: list,
                         bucket: list,
                         lang_code: str,
                         num_proc=4):
    # split the video id lists into n batches
    batches = np.array_split(np.asarray(vid_id_list), num_proc)

    # assign temp buckets for each batches
    # register processes
    with Manager() as manager:
        ns = manager.Namespace()
        ns.shared_bucket = []

        processes = [Process(target=collect_videos, args=(ns, batch, lang_code))
                     for batch in batches]

        # start the processes
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        for video in ns.shared_bucket:
            bucket.append(video)


def exec_indexing_all(channel_url: str,
                      channel_theme: str,
                      lang_code: str,
                      num_proc: int = 4):
    """
    given the channel url,
    index all of the captions & tracks s
    """
    # download the channel's meta data, and make it into a channel object.
    # this may change once you change the logic of dl_channel with a custom one.
    channel = ChannelDownloader.dl_channel(channel_url=channel_url,
                                           channel_theme=channel_theme)
    # index the channel first
    store_channel(channel=channel)

    # download videos
    # make this faster using multiple processes
    video_list: List[Video] = list()

    multiprocess_dl_vids(vid_id_list=channel.vid_id_list,
                         bucket=video_list,
                         lang_code=lang_code,
                         num_proc=num_proc)

    # index videos
    for video in video_list:
        store_video(video)

    # index captions
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            store_caption(caption)

    # and then, index all of the tracks
    # you might need a progress bar..
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            for track in caption.tracks:
                store_track(track)
