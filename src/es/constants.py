# currently the end point of elastic search is set to local host.
# with the port number used by the elastic search.
# change this to AWS endpoint after deploying the engine to AWS.
ES_END_POINT = "http://localhost:9200"

# the name of the database is youtora! obviously..
INDEX = "youtora"

# keyword data type: only searchable by tis exact value
# https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html
# schema for the index above is defined here
INDEX_SCHEMA_DICT = {
    "mappings": {
        "properties": {
            "channel": {
                "properties": {
                    "channel_url": {
                        "type": "keyword"  # 이건 필요없을 수도.
                    },
                    "creator": {
                        "type": "text"
                    },
                    "channel_theme": {
                        "type": "keyword"
                    }
                }  # properties
            },
            "video": {
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "upload_date": {
                        "type": "date"
                    }
                }
            },  # video
            "caption": {
                "properties": {
                    "caption_url": {
                        "type": "keyword"
                    },
                    "caption_type": {
                        "type": "keyword"
                    },
                    "lang_code": {
                        "type": "keyword"
                    }
                }
            },  # caption
            "track": {
                "properties": {
                    "start": {
                        "type": "double"
                    },
                    "duration": {
                        "type": "double"
                    },
                    "text": {
                        "type": "text"
                    }
                }  # properties
            },  # track
            # note: the _parent thing is deprecated in elastic search 7.
            "youtora_relations": {
                "type": "join",  # join data type
                "relations": {
                    "channel": "video",
                    "video": "caption",
                    "caption": "track"
                }
            }
        }
    }  # mappings
}  # data_dict
