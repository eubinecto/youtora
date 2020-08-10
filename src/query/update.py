

from src.es.restAPIs.searchAPIs.search import SearchAPI
from src.main.index import IdxSingle
from src.main.index import Youtora
from src.youtube.dload.dloaders import VideoDownloader
import logging


class UpdateTracks:

    @classmethod
    def update_tracks(cls):
        """
        update all the track fields, except for captions.
        """
        QUERY_GET_ALL_TRACKS = {

        }


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

        # keep these for logging
        total = response['hits']['total']['value']
        done = 0

        # multiprocessing pattern 1
        # get the video ids to update
        vid_id_list = [hit['_id'] for hit in response['hits']['hits']]

        # multiprocessing pattern 2
        # loop through the video ids.
        for vid_id in vid_id_list:
            # download video
            # this will download it with the updated fields
            vid = VideoDownloader.dl_video("https://www.youtube.com/watch?v={}".format(vid_id))

            # index with the new fields
            IdxSingle.idx_video(vid)
            done += 1
            logger.info("{}/{} done.".format(done, total))

