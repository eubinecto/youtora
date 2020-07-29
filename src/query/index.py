# for talking to elastic search
from typing import Generator, List

from src.download.models import Channel, Playlist, Video, Caption, Track

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
        doc = {
            "type": "channel",
            "channel_url": channel.channel_url,
            "uploader": channel.uploader,
            "subscribers": channel.subscribers,
            # "channel_theme": channel.channel_theme, <- maybe later
            # parent-child relationship.
            # channel is the root, so no need for specifying
            # the parent id. (which does not exist)
            "youtora_relations": {
                "name": "channel"
            }
        }
        # send a request to es
        # channel is the root, so no need for for
        # specifying  routing
        IdxAPI.put_doc(index="youtora",
                       _id=channel.channel_id,
                       doc=doc,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # force refresh
                       refresh='true')

    @classmethod
    def idx_playlist(cls, playlist: Playlist):
        # build the doc
        doc = {
            "type": "playlist",
            "plist_url": playlist.plist_url,
            "plist_title": playlist.plist_title,
            "plist_vid_ids": playlist.plist_vid_ids,
            "youtora_relations": {
                "name": "playlist",
                "parent": playlist.plist_channel.channel_id
            }
        }
        # send a request to es
        # channel is the root, so no need for for
        # specifying  routing
        IdxAPI.put_doc(index="youtora",
                       _id=playlist.plist_id,
                       doc=doc,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # must live in the same shard as the parent
                       routing=playlist.plist_channel.channel_id,
                       # force refresh
                       refresh='true')

    @classmethod
    def idx_video(cls, video: Video):
        # include the parent id in data json.

        doc = {
            "type": "video",
            "title": video.vid_title,
            "upload_date": video.upload_date,
            "views": video.views,
            "likes": video.likes,
            "dislikes": video.dislikes,
            "youtora_relations": {
                "name": "video",
                # provide the parent id here
                # a channel is the parent of a video
                "parent": video.channel_id
            }  # relation key
        }  # doc

        # send request
        IdxAPI.put_doc(index="youtora",
                       _id=video.vid_id,
                       doc=doc,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # designate a parent id
                       routing=video.channel_id,
                       # force refresh
                       refresh='true')

    @classmethod
    def idx_caption(cls, caption: Caption):

        # video is the parent of caption
        parent_id = caption.caption_comp_key.split("|")[0]

        # build the data to send to elastic search
        # include the parent id in data json
        doc = {
            "type": "caption",
            "caption_type": caption.caption_type,
            "lang_code": caption.lang_code,
            "caption_url": caption.caption_url,
            "youtora_relations": {
                "name": "caption",
                "parent": parent_id
            }
        }
        # send a request to es
        IdxAPI.put_doc(index="youtora",
                       _id=caption.caption_comp_key,
                       doc=doc,
                       # automatically replaces the doc should it already exists
                       op_type='index',
                       # designate a parent id
                       routing=parent_id,
                       # force refresh (make it immediately visible to search)
                       refresh='true')


def idx_track(track: Track):
    
    # caption is the parent of track
    parent_id = "|".join(track.track_comp_key.split("|")[:-1])

    # build the data to send to elastic search
    # include the parent id in data json
    doc = {
        "type": "track",
        "start": track.start,
        "duration": track.duration,
        "text": track.text,
        "youtora_relations": {
            "name": "track",
            "parent": parent_id
        }
    }
    # make a request to es
    IdxAPI.put_doc(index="youtora",
                   _id=track.track_comp_key,
                   doc=doc,
                   # automatically replaces the doc should it already exists
                   op_type='index',
                   # designate a parent id
                   routing=parent_id,
                   # force refresh
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
                   tracks: List[Track],
                   op_type: str = None):
        """
        uses bulk api to store all the tracks at a single request
        """
        request_body = list()
        # gather up all the docs
        for track in tracks:
            # extract the parent id
            parent_id = "|".join(track.track_comp_key.split("|")[:-1])
            request = {
                "index": {
                    "_index": "youtora",
                    "_id": track.track_comp_key,
                    # you can specify routing point for each action
                    # https://stackoverflow.com/questions/19745515/why-doesnt-routing-work-with-elasticsearch-bulk-api
                    "routing": parent_id
                }  # index
            }  # request
            if op_type:
                assert op_type in API.OP_TYPE_OPS
                request["index"]["op_type"] = op_type
            doc = {
                "type": "track",
                "start": track.start,
                "duration": track.duration,
                "text": track.text,
                "youtora_relations": {
                    "name": "track",
                    "parent": parent_id
                }
            }
            request_body.append(request)
            request_body.append(doc)
            # delete the track once used
            del track

        BulkAPI.post_bulk(request_body=request_body,
                          refresh='true',
                          index="youtora")
