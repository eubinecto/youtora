# for talking to elastic search
from typing import List

import requests

import json

from src.es.utils import log_response
from src.download.downloaders import ChannelDownloader, VideoDownloader
from src.download.models import Channel, Video, Caption, Track

# import all constants
from src.es.constants import *

# for systematic logging
import logging


def create_index(index_name):
    """
    The create index API allows to instantiate an index.
     Elasticsearch provides support for multiple indices,
     including executing operations across several indices.
    https://www.elastic.co/guide/en/elasticsearch/reference/5.6/indices-create-index.html
    """
    r = requests.put(url=ES_END_POINT + "/{}".format(index_name),
                     json=INDEX_SCHEMA_DICT)
    # log it
    log_response(r, "create_index")

    # if no exception is thrown, then return the json
    return r.json()


def create_doc(index: str,
               doc_id: str,
               doc: dict,
               params: dict):
    """
    :param index: the name of the index in which the doc is to be stored
    :param doc_id: unique id of the doc
    :param doc: the doc json dict.
    :param params: additional parameters to pass in to the put request
    """

    # send the indexing request
    query = "/{index}/_doc/{id}" \
        .format(index=index,
                id=doc_id)

    # need to specify the content type in the headers,
    # or else you'll get an error like this:
    # "Content-Type header [application/x-www-form-urlencoded] is not supported",
    headers = {
        "content-type": "application/json"
    }

    # consult pg.39 of the book elastic search the definitive guide
    r = requests.put(url=ES_END_POINT + query,
                     json=doc,
                     params=params,
                     headers=headers)

    # check if the request was successful
    log_response(r, "create_doc")


def create_channel(channel: Channel):
    """
    parent need not be knowing anything about the its children.
    :param channel: a channel object
    """

    # build the data to send to elastic search
    channel_id = channel.channel_id

    # build the doc
    doc = {
        "type": "channel",
        "channel_url": channel.channel_url,
        "creator": channel.creator,
        "channel_theme": channel.channel_theme,
        # parent-child relation ship.
        # channel is the root, so no need for specifying
        # the parent id. (which does not exist)
        "youtora_relations": {
            "name": "channel"
        }
    }

    # what is "refresh" for?
    # it forces to "refresh" the doc with the given id,
    # should it already exists!
    params = {"refresh": ""}

    create_doc(index=INDEX,
               doc_id=channel_id,
               doc=doc,
               params=params)


def create_video(video: Video):
    # channel is the parent of video
    parent_id = video.channel_id

    # build the data to send to elastic search
    vid_id = video.vid_id

    # include the parent id in data json.
    doc = {
        "type": "video",
        "title": video.title,
        "upload_date": video.upload_date,
        "youtora_relations": {
            "name": "video",
            # provide the parent id here
            "parent": parent_id
        }  # relation key
    }  # doc

    params = {
        # this seems important, but why?
        "routing": parent_id,
        "refresh": ""
    }

    create_doc(index=INDEX,
               doc_id=vid_id,
               doc=doc,
               params=params)


def create_caption(caption: Caption):
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
    params = {
        # this seems important, but why?
        "routing": parent_id,
        "refresh": ""
    }

    create_doc(index=INDEX,
               doc_id=caption.caption_comp_key,
               doc=doc,
               params=params)


def create_track(track: Track):
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

    params = {
        # this seems important, but why?
        "routing": parent_id,
        "refresh": ""
    }

    create_doc(index=INDEX,
               doc_id=track.track_comp_key,
               doc=doc,
               params=params)





