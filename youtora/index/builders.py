from youtora.index.indices import (
    ChannelInnerDoc,
    VideoInnerDoc,
    CaptionInnerDoc,
    GeneralIndex
)
from youtora.scrape.dataclasses import VideoData, ChannelData, CaptionData
from youtora.scrape.models import (
    ChannelRaw,
    VideoRaw
)
from youtora.scrape.parsers import (
    ChannelRawParser,
    VideoRawParser

)
from typing import Generator


class GeneralIdxBuilder:
    @classmethod
    def build(cls):
        channels = cls._get_all_channels()
        channels_videos = cls._get_channels_videos(channels)
        # parallel iteration
        for channel, channel_videos in zip(channels, channels_videos):
            channel_doc = cls._build_channel_doc(channel)
            for video in channel_videos:
                video_doc = cls._build_video_doc(video, channel_doc)
                for caption in video.captions:
                    caption_doc = cls._build_caption_doc(caption, video_doc)
                    for track in caption.tracks:
                        general_idx = GeneralIndex(start=track.start, duration=track.duration,
                                                   content=track.content, prev_id=track.prev_id,
                                                   next_id=track.next_id, context=track.context,
                                                   caption=caption_doc)
                        # save it
                        general_idx.save()

    @classmethod
    def _get_all_channels(cls) -> Generator[ChannelData, None, None]:
        # get all the channel_raws
        channel_raws = ChannelRaw.objects.all()
        # get the channels
        channels = (
            ChannelRawParser.parse(channel_raw=channel_raw)
            for channel_raw in channel_raws
        )
        return channels

    @classmethod
    def _get_channels_videos(cls, channels: Generator[ChannelData, None, None]) \
            -> Generator[Generator[VideoData, None, None], None, None]:
        """
        returns a generator of generator of video data
        """
        # get all video raws for channel_raw
        channels_video_raws = (
            VideoRaw.objects.all().filter(channel_id=channel.id)
            for channel in channels
        )
        # parse all of them - this shouldn't take too much time.
        channels_videos = (
            VideoRawParser.parse_multi(video_raw_coll=channel_video_raws)
            for channel_video_raws in channels_video_raws
        )
        return channels_videos

    @classmethod
    def _build_channel_doc(cls, channel: ChannelData) -> ChannelInnerDoc:
        return ChannelInnerDoc(id=channel.id,
                               subs=channel.subs,
                               lang_code=channel.lang_code)

    @classmethod
    def _build_video_doc(cls, video: VideoData, channel_doc: ChannelInnerDoc) -> VideoInnerDoc:
        video_doc = VideoInnerDoc(id=video.id, views=video.views,
                                  likes=video.likes, dislikes=video.dislikes,
                                  category=video.category, channel=channel_doc)
        if video.dislikes > 0:
            video_doc.like_ratio = video.likes / video.dislikes
        return video_doc

    @classmethod
    def _build_caption_doc(cls, caption: CaptionData, video_doc: VideoInnerDoc) -> CaptionInnerDoc:
        caption_doc = CaptionInnerDoc(id=caption.id, is_auto=caption.is_auto,
                                      lang_code=caption.lang_code, video=video_doc)
        return caption_doc
