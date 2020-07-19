
# for creating youtora
from src.es.restAPIs.idxAPIs.idxManagement import CreateIdxAPI


def create_youtora_idx():
    """
    creates the youtora index with the given configurations
    """
    # keyword data type: only searchable by tis exact value
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html
    # schema for the index above is defined here
    mappings = {
        "properties": {
            "channel": {
                "properties": {
                    "channel_url": {
                        "type": "keyword"  # 이건 필요없을 수도.
                    },
                    "creator": {
                        "type": "keyword"
                    }  # creator
                }  # properties
            },  # channel
            "playlist": {
                "properties": {
                    "plist_url": {
                        "type": "keyword"
                    },
                    "plist_title": {
                        "type": "keyword"
                    },
                    "plist_vid_ids": {
                        # of type array. can I leave this as blank?
                        "type": "keyword"
                    }
                }  # properties
            },  # playlist
            "video": {
                "properties": {
                    "vid_title": {
                        "type": "text"
                    },
                    "upload_date": {
                        "type": "date"
                    }
                }  # properties
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
                }  # properties
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
                    # a channel is a parent of both playlist and video
                    "channel":  ["playlist", "video"],
                    "video": "caption",
                    "caption": "track"
                }  # relations
            }  # youtora_relations
        }  # properties
    }  # mappings_config

    # call to es
    CreateIdxAPI.create_idx(index="youtora",
                            mappings=mappings)
