# for talking to elastic search
from typing import List

import requests

import json

from ..download.downloaders import ChannelDownloader, VideoDownloader
from ..download.models import Channel, Video, Caption, Track

# use this client for handling elastic search
from elasticsearch import Elasticsearch

# currently the end point of elastic search is set to local host.
# with the port number used by the elastic search.
# change this to AWS endpoint after deploying the engine to AWS.
ES_END_POINT = "http://localhost:9200"

# the name of the database is youtora! obviously..
INDEX = "youtora"

# schema for the index above is defined here
INDEX_SCHEMA_DICT = {
    "mappings": {
        "properties": {
            "channel": {
                "properties": {
                    "channel_url": {
                        "type": "text"
                    },
                    "creator": {
                        "type": "text"
                    },
                    "channel_theme": {
                        "type": "text"
                    }
                }  # properties
            },
            "video": {
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "channel_id": {
                        "type": "text"
                    },
                    "upload_date": {
                        "type": "date"
                    }
                }
            },  # video
            "caption": {
                "properties": {
                    "caption_url": {
                        "type": "text"
                    },
                    "caption_type": {
                        "type": "text"
                    },
                    "lang_code": {
                        "type": "text"
                    }
                }
            },  # caption
            "track": {
                "properties": {
                    "start": {
                        "type": "double"
                    },
                    "duration": {
                        "type": "double"
                    },
                    "text": {
                        "type": "text"
                    }
                }  # properties
            },  # track
            # note: the _parent thing is deprecated in elastic search 7.
            "channel_relations": {
                "type": "join",
                "relations": {
                    "channel": "video",
                    "video": "caption",
                    "caption": "track"
                }
            }
        }
    }  # mappings
}  # data_dict


def es_index_doc(doc_type,
                 doc_id,
                 doc):
    # send the indexing request
    global INDEX
    query_index_doc = "/{index}/{type}/{id}" \
        .format(index=INDEX,
                type=doc_type,
                id=doc_id)

    # consult pg.39 of the book elastic search the definitive guide
    r = requests.put(url=ES_END_POINT + query_index_doc,
                     data=doc)

    # check if the request was successful
    r.raise_for_status()


def index_channel(channel: Channel):
    """
    parent need not be knowing anything about the its children.
    :param channel: a channel object
    """

    # build the data to send to elastic search
    channel_id = channel.channel_id
    doc = {}

    es_index_doc(doc_type="channel",
                 doc_id=channel_id,
                 doc=doc)


def index_video(video: Video):
    # channel is the parent of video
    parent_id = video.channel_id
    parent_type = "channel"

    # build the data to send to elastic search
    vid_id = video.vid_id

    # include the parent id in data json.
    doc = {}

    es_index_doc(doc_type="video",
                 doc_id=vid_id,
                 doc=doc)


def index_caption(caption: Caption):
    # video is the parent of caption
    parent_id = caption.caption_comp_key.split("|")[0]
    parent_type = "video"

    # build the data to send to elastic search
    # include the parent id in data json
    doc = {}

    es_index_doc(doc_type="caption",
                 doc_id=caption.caption_comp_key,
                 doc=doc)


def index_track(track: Track):
    # caption is the parent of track
    parent_id = track.track_comp_key.split("|")[0]
    parent_type = "caption"

    # build the data to send to elastic search
    # include the parent id in data json
    doc = {}

    es_index_doc(doc_type=track,
                 doc_id=track.track_comp_key,
                 doc=doc)


def exec_indexing_all(channel_url: str,
                      channel_theme: str):
    """
    given the channel url,
    index all of the captions & tracks s
    """
    # download the channel's meta data, and make it into a channel object.
    # this may change once you change the logic of dl_channel with a custom one.
    channel = ChannelDownloader.dl_channel(channel_url=channel_url,
                                           channel_theme=channel_theme)
    # index the channel first
    index_channel(channel=channel)

    # download videos
    video_list: List[Video] = list()
    for vid_id in channel.vid_id_list:
        # make a vid_url
        vid_url = "https://www.youtube.com/watch?v={}" \
            .format(vid_id)
        video_list.append(VideoDownloader.dl_video(vid_url=vid_url))

    # index videos
    for video in video_list:
        index_video(video)

    # index captions
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            index_caption(caption)

    # and then, index all of the tracks
    for video in video_list:
        for caption_type, caption in video.captions.items():
            caption_type: str
            caption: Caption
            for track in caption.tracks:
                index_track(track)


def create_index(index_name):
    """
    helper function to be used for creating an index with s
    """
    global ES_END_POINT
    global INDEX_SCHEMA_DICT

    r = requests.put(url=ES_END_POINT + "/{}".format(index_name),
                     json=INDEX_SCHEMA_DICT)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as he:
        # print the error
        print(he)
        print(json.dumps(r.json(), indent=2))
    else:
        print(json.dumps(r.json(), indent=2))
    # wait, how do I do logging in python?
    # for logging


