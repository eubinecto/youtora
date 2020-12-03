import json
import logging
import os
import sys
from typing import Generator, List

from django.core.exceptions import ObjectDoesNotExist
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search
from termcolor import colored

from youtora.collect.models import (
    ChannelRaw,
    VideoRaw,
    TracksRaw
)
from youtora.index.docs import (
    es_client,
    ChannelInnerDoc,
    VideoInnerDoc,
    CaptionInnerDoc,
    GeneralDoc,
    OpenSubDoc,  # for searching opensub data.
)
from youtora.refine.dataclasses import Video, Channel, Caption
from youtora.refine.extractors import (
    ChannelExtractor,
    VideoExtractor,
    CaptionExtractor,
    TrackExtractor
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# es logger is too verbose. set the logging level to warning.
# https://stackoverflow.com/a/47157553
es_logger = logging.getLogger("elasticsearch")
es_logger.setLevel(logging.WARNING)  # suppress the logs from es_client.


class BuildGeneralIdx:
    VIDEO_BATCH_SIZE = 10
    IDX_NAME = GeneralDoc.Index.name

    @classmethod
    def exec(cls, channel_id: str):
        logger = logging.getLogger("exec")
        cls._delete_by_channel_id(channel_id)  # delete all tracks that belong to this channel
        channel_raw = ChannelRaw.objects.get(_id=channel_id)  # get the channel_raw
        # parse the channel_raw and build the doc
        channel = ChannelExtractor.parse(channel_raw)
        channel_doc = cls._build_channel_doc(channel)
        # filtering
        vid_qset = VideoRaw.objects.filter(channel_id=channel_raw.id)
        batches = cls._batched_queryset(vid_qset)  # to use elasticsearch-dsl's  bulk API.
        vid_cnt = vid_qset.count()  # for progress report
        for batch_idx, batch_qset in enumerate(batches):
            for vid_idx, video_raw in enumerate(batch_qset):
                # parse the video_raw and build the doc
                video = VideoExtractor.parse(video_raw)
                video_doc = cls._build_video_doc(video, channel_doc)
                # extract captions from this
                captions = CaptionExtractor.parse(video_raw)
                general_doc_dicts = cls._build_general_doc_dicts(captions, video_doc)
                bulk(client=es_client, actions=general_doc_dicts)
                # log progress.
                vid_saved = batch_idx * cls.VIDEO_BATCH_SIZE + (vid_idx + 1)
                msg = "saved:all_tracks:video={}/{}:channel={}" \
                    .format(vid_saved, vid_cnt, str(channel))
                logger.info(colored(msg, 'blue'))

    @classmethod
    def exec_multi(cls):
        """
        build indices for all channels stored
        :return:
        """
        for chan_raw in ChannelRaw.objects.iterator():
            cls.exec(chan_raw.id)

    @classmethod
    def _build_channel_doc(cls, channel: Channel) -> ChannelInnerDoc:
        return ChannelInnerDoc(id=channel.id,
                               subs=channel.subs,
                               lang_code=channel.lang_code)

    @classmethod
    def _build_video_doc(cls, video: Video, channel_doc: ChannelInnerDoc) -> VideoInnerDoc:
        publish_date_int = "".join(video.publish_date.split("-"))
        video_doc = VideoInnerDoc(id=video.id, views=video.views, title=video.title,
                                  publish_date_int=publish_date_int,
                                  category=video.category, channel=channel_doc)
        return video_doc

    @classmethod
    def _build_caption_doc(cls, caption: Caption, video_doc: VideoInnerDoc) -> CaptionInnerDoc:
        caption_doc = CaptionInnerDoc(id=caption.id, is_auto=caption.is_auto,
                                      lang_code=caption.lang_code, video=video_doc)
        return caption_doc

    @classmethod
    def _build_general_doc_dicts(cls, captions: List[Caption], video_doc: VideoInnerDoc) \
            -> Generator[dict, None, None]:
        """
        for passing it to bulk helper
        # reference:
        # https://github.com/elastic/elasticsearch-dsl-py/issues/403#issuecomment-218447768
        :return:
        """
        logger = logging.getLogger("_build_general_doc_dicts")
        for cap_idx, caption in enumerate(captions):
            # build caption doc
            caption_doc = cls._build_caption_doc(caption, video_doc)
            # get the tracks raw for this caption
            try:
                tracks_raw = TracksRaw.objects.get(caption_id=caption.id)
            except ObjectDoesNotExist as bde:
                logger.warning(str(bde))
                logger.warning("SKIP:tracks_raw does not exist for:caption_id=" + caption.id)
                continue
            else:
                # parse it to get all tracks
                tracks = TrackExtractor.parse(tracks_raw)
                # send all the tracks in the captions to the generator
                for track in tracks:
                    general_doc = GeneralDoc(meta={'id': track.id},  # this is how you put the id
                                             start=track.start, duration=track.duration,
                                             content=track.content, prev_id=track.prev_id,
                                             next_id=track.next_id, context=track.context,
                                             caption=caption_doc)
                    # turn them into dicts to be passed to bulk helper
                    general_doc_dict = general_doc.to_dict(include_meta=True)
                    # and yield
                    yield general_doc_dict

    @classmethod
    def _batched_queryset(cls, queryset):
        """
        Slice a queryset into chunks.
        Code excerpted from: https://djangosnippets.org/snippets/10599/
        """
        start_pk = 0
        queryset = queryset.order_by('pk')
        while True:
            # No entry left
            if not queryset.filter(pk__gt=start_pk).exists():
                break
            try:
                # Fetch chunk_size entries if possible
                end_pk = queryset.filter(pk__gt=start_pk).values_list(
                    'pk', flat=True)[cls.VIDEO_BATCH_SIZE - 1]
                # Fetch rest entries if less than chunk_size left
            except IndexError:
                end_pk = queryset.values_list('pk', flat=True).last()
            yield queryset.filter(pk__gt=start_pk).filter(pk__lte=end_pk)
            start_pk = end_pk

    @classmethod
    def _delete_by_channel_id(cls, channel_id: str) -> dict:
        s: Search = Search(index=cls.IDX_NAME) \
            .query("match", **{"caption.video.channel.id": channel_id})
        resp = s.delete()
        return resp.to_dict()


# for opensub
class BuildOpenSubIdx:
    # to be used for es_client.
    IDX_NAME = OpenSubDoc.Index.name
    NUM_PROC = 5
    NDJSON_BATCH_SIZE = 30  # the size of each batch to be sent with a bulk call

    @classmethod
    def exec(cls, splits_ndjson_dir: str):
        logger = logging.getLogger("build_idx_by_bulk")
        # what should you do?
        # first, get all the file names
        file_paths = [
            os.path.join(splits_ndjson_dir, ndjson_file_name)
            for ndjson_file_name in os.listdir(splits_ndjson_dir)  # this returns a list of file name.
        ]
        batches = cls.chunks(file_paths, cls.NDJSON_BATCH_SIZE)
        for idx, batch in enumerate(batches):
            cls.build_idx_by_bulk(batch)
            msg = colored("Batch done={}/{}".format(idx, len(batches)), 'blue')
            logger.info(msg)

    @classmethod
    def build_idx_by_bulk(cls, file_path_batch: List[str]):
        print(file_path_batch)
        # Here, you split the paths by batches.
        # build dicts
        opensub_doc_dicts = (
            opensub_dict
            for file_path in file_path_batch
            for opensub_dict in cls.build_opensub_doc_dicts(file_path)
        )
        # build index by bulk call
        bulk(client=es_client, actions=opensub_doc_dicts)

    @classmethod
    def build_opensub_doc_dicts(cls, file_path: str) -> Generator[dict, None, None]:
        with open(file_path, 'r') as fh:
            for line in fh:
                example: dict = json.loads(line)
                response: str = example['response']
                contexts: List[str] = example['contexts']
                example_id = file_path.split("/")[-1].replace(".ndjson", "")
                opensub_doc = OpenSubDoc(meta={'id': example_id},  # use the path as the id.
                                         response=response, contexts=contexts)
                yield opensub_doc.to_dict(include_meta=True)

    @staticmethod
    def chunks(lst, n) -> list:
        """Yield successive n-sized chunks from lst."""
        return [
            lst[i:i + n]
            for i in range(0, len(lst), n)
        ]
