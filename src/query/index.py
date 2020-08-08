# for talking to elastic search
from typing import Generator, List

from src.query.create import IdxQuery
from src.youtube.dload.models import Channel, Video, Caption, Track

# API for indexing a single document
from src.es.restAPIs.API import API
from src.es.restAPIs.docAPIs.single import IdxAPI
from src.es.restAPIs.docAPIs.multi import BulkAPI


class IdxSingle:
    @classmethod
    def idx_channel(cls, channel: Channel):
        """
        parent need not be knowing anything about the its children.
        :param channel: a channel object
        """
        # build the doc
        doc_body = {
            "doc_type": "channel",
            "url": channel.url,
            "title": channel.title,
            "subs": channel.subs,
        }
        # send a request to es
        # channel is the root, so no need for for
        # specifying  routing
        IdxAPI.put_doc(index=IdxQuery.YOUTORA_COLL_IDX_NAME,
                       _id=channel.channel_id,
                       doc=doc_body,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # force refresh (immediately visible by search)
                       refresh='true')

    @classmethod
    def idx_video(cls, video: Video):
        # include the parent id in data json.

        doc_body = {
            "doc_type": "video",
            "url": video.url,
            "title": video.title,
            "publish_date": video.publish_date,
            # store it as an int, to be used as a ranking feature
            "publish_date_int": int("".join(video.publish_date.split("-"))),
            "views": video.views,
            "likes": video.likes,
            "dislikes": video.dislikes,
            # in case of zero division, the value should be -1
            "like_ratio": -1 if video.likes == 0 and video.dislikes == 0
            else video.likes / (video.dislikes + video.likes)
        }  # doc

        # send request
        IdxAPI.put_doc(index=IdxQuery.YOUTORA_COLL_IDX_NAME,
                       _id=video.vid_id,
                       doc=doc_body,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # force refresh
                       refresh='true')

    @classmethod
    def idx_caption(cls, caption: Caption):

        # video is the parent of caption
        parent_id = caption.caption_comp_key.split("|")[0]

        # build the data to send to elastic search
        # include the parent id in data json
        doc_body = {
            "doc_type": "caption",
            "url": caption.url,
            "lang_code": caption.lang_code,
            "is_auto": caption.is_auto
        }
        # send a request to es
        IdxAPI.put_doc(index=IdxQuery.YOUTORA_COLL_IDX_NAME,
                       _id=caption.caption_comp_key,
                       doc=doc_body,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # designate a parent id
                       # force refresh (make it immediately visible to search)
                       refresh='true')


class IdxMulti:
    """
    use these to reduce request overhead.
    you might want to define generators.
    """
    @classmethod
    def idx_videos(cls, videos: Generator[Video, None, None]):
        """
        uses bulk api to store all the videos at a single request
        """
        # fill this in later by using generators.
        pass

    @classmethod
    def idx_captions(cls, captions: Generator[Caption, None, None]):
        # fill this in later
        # using generators
        pass

    @classmethod
    def idx_tracks(cls,
                   caption: Caption,
                   video: Video,
                   channel: Channel,
                   op_type: str = None):

        """
        uses bulk api to index all the tracks at once.
        :param caption: the caption that the track belongs to
        :param video: the video that the track belongs to
        :param channel: the channel that the track belongs to
        :param op_type: ...?
        """
        # get the tracks
        tracks = caption.tracks
        # build a request body
        request_body = list()
        # gather up all the docs
        for track in tracks:
            # extract the parent id
            parent_id = "|".join(track.track_comp_key.split("|")[:-1])
            query = {
                "index": {
                    "_index": IdxQuery.YOUTORA_TRACKS_IDX_NAME,
                    "_id": track.track_comp_key,
                }  # index
            }  # query
            if op_type:
                assert op_type in API.OP_TYPE_OPS
                query["index"]["op_type"] = op_type
            doc_body = {
                "doc_type": "track",
                "start": track.start,
                "duration": track.duration,
                "content": track.content,
                "caption": {
                    "id": caption.caption_comp_key,
                    "is_auto": caption.is_auto,
                    "lang_code": caption.lang_code,
                    "video": {
                        "id": video.vid_id,
                        "views": video.views,
                        "likes": video.likes,
                        "dislikes": video.dislikes,
                        # if if their sum is zero, then the value defaults to -1.
                        "like_ratio": -1 if (video.likes + video.dislikes) == 0
                        else video.likes / (video.dislikes + video.likes),
                        "publish_date_int": int("".join(video.publish_date.split("-"))),
                        "channel": {
                            "id": channel.channel_id,
                            "subs": channel.subs
                        }  # channel
                    }  # video
                }  # caption
            }  # doc_body
            request_body.append(query)
            request_body.append(doc_body)
            # delete the track once used
            del track

        # call to the es
        BulkAPI.post_bulk(request_body=request_body,
                          # immediately searchable
                          refresh='true',
                          index=IdxQuery.YOUTORA_TRACKS_IDX_NAME)
