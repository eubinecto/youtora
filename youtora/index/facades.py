import logging
import sys
from typing import Generator, List

from elasticsearch.helpers import bulk

from youtora.collect.models import (
    ChannelRaw,
    VideoRaw,
    TracksRaw
)
from youtora.index.docs import (
    ChannelInnerDoc,
    VideoInnerDoc,
    CaptionInnerDoc,
    GeneralDoc
)
from youtora.index.docs import es_client
from youtora.refine.dataclasses import Video, Channel, Caption, Track
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
es_logger.setLevel(logging.WARNING)


class BuildGeneralDoc:
    @classmethod
    def exec(cls):
        logger = logging.getLogger("build")
        channel_raws = ChannelRaw.objects.all()
        for chan_idx, channel_raw in enumerate(channel_raws):
            # parse the channel_raw and build the doc
            channel = ChannelExtractor.parse(channel_raw)
            channel_doc = cls._build_channel_doc(channel)
            video_raws = VideoRaw.objects.filter(channel_id=channel_raw.id)
            for vid_idx, video_raw in enumerate(video_raws):
                # parse the video_raw and build the doc
                video = VideoExtractor.parse(video_raw)
                video_doc = cls._build_video_doc(video, channel_doc)
                # extract captions from this
                captions = CaptionExtractor.parse(video_raw)
                for cap_idx, caption in enumerate(captions):
                    # build caption doc
                    caption_doc = cls._build_caption_doc(caption, video_doc)
                    # get the tracks raw for this caption
                    tracks_raw = TracksRaw.objects.get(caption_id=caption.id)
                    # parse it to get all tracks
                    tracks = TrackExtractor.parse(tracks_raw)
                    general_doc_dicts = cls._build_general_doc_dicts(tracks, caption_doc)
                    bulk(client=es_client, actions=general_doc_dicts)
                    logger.info("saved:channel={}|{}:video={}|{}:caption={}|{}:all tracks"
                                .format(chan_idx, str(channel), vid_idx, str(video),
                                        cap_idx, str(caption)))

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
    def _build_general_doc_dicts(cls, tracks: List[Track], caption_doc: CaptionInnerDoc) \
            -> Generator[dict, None, None]:
        """
        for passing it to bulk helper
        # reference:
        # https://github.com/elastic/elasticsearch-dsl-py/issues/403#issuecomment-218447768
        :param tracks:
        :param caption_doc:
        :return:
        """
        general_docs = (
            GeneralDoc(meta={'id': track.id},  # this is how you put the id
                       start=track.start, duration=track.duration,
                       content=track.content, prev_id=track.prev_id,
                       next_id=track.next_id, context=track.context,
                       caption=caption_doc)
            for track in tracks
        )
        # turn them into dicts to be passed to bulk helper
        dicts = (
            general_doc.to_dict(include_meta=True)
            for general_doc in general_docs
        )
        return dicts
