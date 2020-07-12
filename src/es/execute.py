import logging
from typing import List

from src.download.downloaders import ChannelDownloader, VideoDownloader
from src.download.models import Video, Caption
from src.es.crud.create import create_channel, create_video, create_caption, create_track

# for faster video download
from multiprocessing import Process


def exec_indexing_all(channel_url: str,
                      channel_theme: str,
                      lang_code: str):
    """
    given the channel url,
    index all of the captions & tracks s
    """
    # download the channel's meta data, and make it into a channel object.
    # this may change once you change the logic of dl_channel with a custom one.
    channel = ChannelDownloader.dl_channel(channel_url=channel_url,
                                           channel_theme=channel_theme)
    # index the channel first
    create_channel(channel=channel)

    # download videos
    # make this faster using multiple processes
    video_list: List[Video] = list()
    total_vid_cnt = len(channel.vid_id_list)
    vid_done = 0
    vid_logger = logging.getLogger("video_list")

    # 여기를 multi-processing 으로?
    # 어떻게 할 수 있는가?
    for vid_id in channel.vid_id_list:
        # make a vid_url
        vid_url = "https://www.youtube.com/watch?v={}" \
            .format(vid_id)
        video_list.append(VideoDownloader.dl_video(vid_url=vid_url,
                                                   lang_code=lang_code))
        vid_done += 1
        vid_logger.info("video done: {}/{}".format(vid_done, total_vid_cnt))

    # target = the for loop above
    # arg = 1. container, and ,mini batch.
    # start all of the process
    # join all of the  process

    # index videos
    for video in video_list:
        create_video(video)

    # index captions
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            create_caption(caption)

    # and then, index all of the tracks
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            for track in caption.tracks:
                create_track(track)
