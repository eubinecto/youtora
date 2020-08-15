from src.elastic.query.create import Youtora
from src.elastic.restAPIs.docAPIs.multi import BulkAPI


class Stash:
    """
    stashes data to elastic search
    """
    @classmethod
    def stash_tracks(cls):
        # we want to build a request body
        request_body = list()
        # get all the tracks
        # this is going to consume A LOT OF SPACE.
        # we have to use logstash for this I think...
        tracks_list = ...
        for track in tracks_list:
            # get the caption, video, and channel that the track belongs to
            # by using the parent id references
            caption = ...
            video = ...
            channel = ...
            # then go on
            # gather up all the docs
            # extract the parent id
            query = {
                "index": {
                    "_index": Youtora.YOUTORA_TRACKS_IDX_NAME,
                    "_id": track.track_comp_key,
                }  # index
            }  # query
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
                        "publish_date_int": int("".join(video.publish_date.split("-"))),
                        "category": video.category,
                        "channel": {
                            "id": channel.channel_id,
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
                    doc_body['caption']['video']['like_ratio']: float = video.likes / (video.likes + video.dislikes)
                # dislike cnt
                if video.dislikes > 0:
                    # add dislike cnt
                    doc_body['caption']['video']['dislikes'] = video.dislikes

            # append to the request
            request_body.append(query)
            request_body.append(doc_body)
            # delete the track once used
            del track

        # call to the es
        BulkAPI.post_bulk(request_body=request_body,
                          # immediately searchable
                          refresh='true',
                          index=Youtora.YOUTORA_TRACKS_IDX_NAME)

    @classmethod
    def stash_chapters(cls):
        """
        do this later.
        :return:
        """
        pass
