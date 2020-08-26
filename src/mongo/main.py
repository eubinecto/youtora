from pymongo.cursor import Cursor

from src.elastic.settings import YOUTORA_TRACKS_IDX_NAME
from src.elastic.restAPIs.docAPIs.multi import BulkAPI
from src.mongo.settings import YoutoraMongo

import logging


class Stash:
    """
    stashes data to elasticsearch index
    """
    # Number of tracks to stash at a time
    STASH_BATCH_SIZE = 100000
    # global access point
    youtora_mongo: YoutoraMongo = None

    @classmethod
    def stash_tracks(cls):
        # set up the handlers for the mongodb
        cls.youtora_mongo = YoutoraMongo()
        logger = logging.getLogger("stash_tracks")
        # we want to build this request body
        request_body = list()
        # get all the tracks
        total_track_num = cls.youtora_mongo.track_coll.estimated_document_count()
        track_coll_cursor: Cursor = cls.youtora_mongo.track_coll.find()
        for idx, track in enumerate(track_coll_cursor):
            track: dict  # the result is a dictionary.
            # get the caption, video, and channel that the track belongs to
            # by using the parent id references
            caption: dict = cls.youtora_mongo.caption_coll.find_one(filter={"_id": track['parent_id']})
            video: dict = cls.youtora_mongo.video_coll.find_one(filter={"_id": caption['parent_id']})
            channel: dict = cls.youtora_mongo.channel_coll.find_one(filter={"_id": video['parent_id']})
            # build the query
            query = {
                "index": {
                    "_index": YOUTORA_TRACKS_IDX_NAME,
                    "_id": track["_id"],
                }  # index
            }  # query
            # build the doc_body
            doc_body = {
                "start": track['start'],
                "duration": track['duration'],
                "content": track['content'],
                "caption": {
                    "id": caption['_id'],
                    "is_auto": caption['is_auto'],
                    "lang_code": caption['lang_code'],
                    "video": {
                        "id": video['_id'],
                        "views": video['views'],
                        "publish_date_int": int("".join(video['publish_date'].split("-"))),
                        "category": video['category'],
                        "channel": {
                            "id": channel['_id'],
                            "subs": channel['subs'],
                            "lang_code": channel['lang_code']
                        }  # channel
                    }  # video
                }  # caption
            }  # doc_body
            # add likes & dislikes only if they are greater than zero.
            if video['likes'] > 0 or video['dislikes'] > 0:
                if video['likes'] > 0:
                    # add like cnt
                    doc_body['caption']['video']['likes'] = video['likes']
                    # like ratio must be greater than zero as well
                    doc_body['caption']['video']['like_ratio']: float \
                        = video['likes'] / (video['likes'] + video['dislikes'])
                # dislike cnt
                if video['dislikes'] > 0:
                    # add dislike cnt
                    doc_body['caption']['video']['dislikes'] = video['dislikes']
            # append to the request
            request_body.append(query)
            request_body.append(doc_body)
            # call to the es when the request body is of the batch size
            if (idx + 1) % cls.STASH_BATCH_SIZE == 0:
                BulkAPI.post_bulk(request_body=request_body,
                                  # immediately searchable
                                  refresh='true',
                                  index=YOUTORA_TRACKS_IDX_NAME)
                # then reset the request_body
                # and continue
                del request_body
                request_body = list()
                continue
            else:
                logger.info("{}/{}: accessing track: {}".format(idx + 1, total_track_num, track['_id']))
            del track  # delete the track once used
        else:
            # on finishing the iteration of track
            if len(request_body):
                BulkAPI.post_bulk(request_body=request_body,
                                  # immediately searchable
                                  refresh='true',
                                  index=YOUTORA_TRACKS_IDX_NAME)
