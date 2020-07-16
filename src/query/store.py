# for talking to elastic search
from src.download.models import Channel, Video, Caption, Track

# API for indexing a single document
from src.es.restAPIs.docAPIs.single import IdxAPI


def store_channel(channel: Channel):
    """
    parent need not be knowing anything about the its children.
    :param channel: a channel object
    """
    # build the doc
    doc = {
        "type": "channel",
        "channel_url": channel.channel_url,
        "creator": channel.creator,
        "channel_theme": channel.channel_theme,
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
                   # force refresh
                   refresh=True)


def store_video(video: Video):
    # include the parent id in data json.
    
    doc = {
        "type": "video",
        "title": video.title,
        "upload_date": video.upload_date,
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
                   # designate a parent id
                   routing=video.channel_id,
                   # force refresh
                   refresh=True)


def store_caption(caption: Caption):
    
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
                   # designate a parent id
                   routing=parent_id,
                   # force refresh
                   refresh=True)


def store_track(track: Track):
    
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
                   # designate a parent id
                   routing=parent_id,
                   # force refresh
                   refresh=True)
