
# for creating youtora
from src.es.restAPIs.idxAPIs.idxManagement import CreateIdxAPI

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
              "l_to_d": {
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
      "l_to_d": {
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


def create_youtora_idx():
    """
    creates the youtora index with the given configurations
    """
    global YOUTORA_TRACKS_IDX_MAPPINGS
    global YOUTORA_COLL_IDX_MAPPINGS

    # create youtora_tracks
    # de-normalisation of the fields.
    CreateIdxAPI.create_idx(index="youtora_tracks",
                            mappings=YOUTORA_TRACKS_IDX_MAPPINGS)

    # create youtora_coll
    CreateIdxAPI.create_idx(index="youtora_coll",
                            mappings=YOUTORA_COLL_IDX_MAPPINGS)



