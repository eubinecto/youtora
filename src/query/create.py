
# for creating youtora
from src.es.restAPIs.idxAPIs.idxManagement import CreateIdxAPI


class IdxQuery:
    YOUTORA_TRACKS_IDX_NAME = "youtora_tracks"
    YOUTORA_TRACKS_IDX_MAPPINGS = {
      "mappings": {
        "properties": {
          "start": {
            "type": "double"
          },
          "duration": {
            "type": "double"
          },
          "content": {
            "type": "text"
          },
          "caption": {
            "properties": {
              "id": {
                # keyword data type: only searchable by the exact value
                # https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html
                "type": "keyword"
              },
              "is_auto": {
                "type" : "boolean"
              },
              "lang_code": {
                "type": "keyword"
              },
              "video": {
                "properties": {
                  "id": {
                    "type": "keyword"
                  },
                  "views": {
                    "type": "rank_feature"
                  },
                  "likes": {
                    "type": "rank_feature"
                  },
                  "dislikes": {
                    "type": "rank_feature",
                    "positive_score_impact": False
                  },
                  "like_ratio": {
                    "type": "rank_feature"
                  },
                  "publish_date_int": {
                    "type": "rank_feature"
                  },
                  "channel": {
                    "properties": {
                      "id": {
                        "type": "keyword"
                      },
                      "subs": {
                        "type": "rank_feature"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

    YOUTORA_COLL_IDX_NAME = "youtora_coll"
    YOUTORA_COLL_IDX_MAPPINGS = {
      "mappings": {
        "properties": {
          "doc_type": {
            "type": "keyword"
          },
          "url": {
            "type": "keyword"
          },
          "title": {
            "type": "text"
          },
          "lang_code": {
            "type": "keyword"
          },
          "is_auto": {
            "type": "boolean"
          },
          "views": {
            "type": "integer"
          },
          "dislikes": {
            "type": "integer"
          },
          "like_ratio": {
            "type": "integer"
          },
          "publish_date": {
            "type": "date"
          },
          "publish_date_int": {
            "type": "integer"
          }
        }
      }
    }

    @classmethod
    def create_youtora_idx(cls):
        """
        creates the youtora index with the given configurations
        """
        # create youtora_tracks
        # de-normalisation of the fields.
        CreateIdxAPI.create_idx(index=cls.YOUTORA_TRACKS_IDX_NAME,
                                mappings=cls.YOUTORA_TRACKS_IDX_MAPPINGS)

        # create youtora_coll
        CreateIdxAPI.create_idx(index=cls.YOUTORA_COLL_IDX_NAME,
                                mappings=cls.YOUTORA_COLL_IDX_MAPPINGS)



