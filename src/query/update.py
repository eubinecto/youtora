

from src.es.restAPIs.searchAPIs.search import SearchAPI
from src.main.index import IdxSingle
from src.main.index import Youtora
from src.youtube.dload.dloaders import VideoDownloader
import logging

class UpdateTracks:

    @classmethod
    def update_videos(cls):
        pass


class UpdateColl:

    QUERY_GET_ALL_VIDEOS = {
        "bool": {
          "must": [
            {
              "match_all": {}
            }
          ],
          "filter": [
            {
              "term": {
                "doc_type": "video"
              }
            }
          ]
        }
    }

    @classmethod
    def update_videos(cls):
        """
        yeah! this is how you update videos anyway.
        refresh all the data upto date.
        :return:
        """
        # get all the videos
        # for each video
        logger = logging.getLogger("update_videos")

        response = SearchAPI.get_search(query=cls.QUERY_GET_ALL_VIDEOS,
                                        index=Youtora.YOUTORA_COLL_IDX_NAME)

        total = response['hits']['total']['value']

        done = 0
        for hit in response['hits']['hits']:
            vid_id = hit['_id']
            # download video
            # this will download it with the updated fields
            vid = VideoDownloader.dl_video("https://www.youtube.com/watch?v={}".format(vid_id))

            # index with the new fields
            IdxSingle.idx_video(vid)
            done += 1
            logger.info("{}/{} done.".format(done, total))

