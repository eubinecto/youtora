from typing import List

from src.elastic.restAPIs.docAPIs.multi import BulkAPI
from src.elastic.settings import YOUTORA_TRACKS_IDX_NAME
from src.youtora.youtube.models import Channel, Video


class Index:

    @classmethod
    def index_tracks(cls,
                     channel: Channel,
                     videos: List[Video]):
        for video in videos:
            # init a bucket
            request_body = list()
            for caption in video.captions:
                for track in caption.tracks:
                    # build the query
                    query = {
                        "index": {
                            "_index": YOUTORA_TRACKS_IDX_NAME,
                            "_id": track.id,
                        }  # index
                    }  # query
                    # build the doc_body
                    doc_body = {
                        "start": track.start,
                        "duration": track.duration,
                        "content": track.content,
                        "caption": {
                            "_id": caption.id,
                            "is_auto": caption.is_auto,
                            "lang_code": caption.lang_code,
                            "video": {
                                "_id": video.id,
                                "views": video.views,
                                "publish_date_int": int("".join(video.publish_date.split("-"))),
                                "category": video.category,
                                "channel": {
                                    "_id": channel.id,
                                    "subs": channel.subs,
                                    "lang_code": channel.lang_code
                                }  # channel
                            }  # video
                        }  # caption
                    }  # doc_body
                    # add likes & dislikes only if they are greater than zero.
                    if video.likes > 0 or video.dislikes > 0:
                        if video.likes > 0:
                            # add like cnt
                            doc_body['caption']['video']['likes'] = video.likes
                            # like ratio must be greater than zero as well
                            doc_body['caption']['video']['like_ratio']: float \
                                = video.likes / (video.likes + video.dislikes)
                        # dislike cnt
                        if video.dislikes > 0:
                            # add dislike cnt
                            doc_body['caption']['video']['dislikes'] = video.dislikes
                    # append to the request
                    request_body.append(query)
                    request_body.append(doc_body)

            else:  # after all captions are complete for this video
                # store the index to
                BulkAPI.post_bulk(request_body=request_body,
                                  # immediately searchable
                                  refresh='true',
                                  index=YOUTORA_TRACKS_IDX_NAME)
                # reset the request body
                del request_body

