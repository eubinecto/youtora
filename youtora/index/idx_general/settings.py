
# list of nodes we should connect to.
# using the eubinCloud's internal IP
HOSTS = [{"host": "localhost", "port": 9200}]
# common attributes
CHANNEL_MAPPINGS = {
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

VIDEO_MAPPINGS = {
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
              "channel": CHANNEL_MAPPINGS
            }
          }

CAPTION_MAPPINGS = {
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
          "video": VIDEO_MAPPINGS
        }
      }

# index to store the tracks
YOUTORA_IDX_MAPPINGS = {
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
      "prev_id": {
        "type": "keyword"
      },
      "next_id": {
        "type": "keyword"
      },
      "context": {
        "type": "text"
      },
      "caption": CAPTION_MAPPINGS
    }
  }
}

YOUTORA_IDX_NAME = "youtora_idx"

