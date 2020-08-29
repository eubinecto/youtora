
# list of nodes we should connect to.
HOSTS = [{"host": "localhost", "port": 9200}]

# index to store the tracks
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
      "text_area_rel_img": {
        "type": "rank_feature"
      },
      "non_text_area_rel_img": {
        "type": "rank_feature"
      },
      "caption": {
        "properties": {
          "id": {
            # keyword data type: only searchable by the exact value
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html
            "type": "keyword"
          },
          "is_auto": {
            "type": "boolean"
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
              "category": {
                "type": "text"
              },
              "channel": {
                "properties": {
                  "id": {
                    "type": "keyword"
                  },
                  "subs": {
                    "type": "rank_feature"
                  },
                  "lang_code": {
                    "type": "keyword"
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

