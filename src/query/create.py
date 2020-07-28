
# for creating youtora
from src.es.restAPIs.idxAPIs.idxManagement import CreateIdxAPI

# the index to store documents in
INDEX_NAME = "doc_ori_youtora"


def create_youtora():
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
                    },
                    "tracks": {
                        # nested type
                        # https://stackoverflow.com/questions/26258292/querystring-search-on-array-elements-in-elastic-search
                        "type": "nested",
                        "properties": {
                            "start": {
                                "type": "double"
                            },
                            "duration": {
                                "type": "double"
                            },
                            "text": {
                                "type": "text"
                            }  #text
                        }  # properties
                    }  # tracks
                }  # properties
            },  # caption
            # note: the _parent thing is deprecated in elastic search 7.
            "youtora_relations": {
                "type": "join",  # join data type
                "relations": {
                    # a channel is a parent of both playlist and video
                    "channel":  ["playlist", "video"],
                    "video": "caption",
                }  # relations
            }  # youtora_relations
        }  # properties
    }  # mappings_config

    # call to es
    CreateIdxAPI.create_idx(index=INDEX_NAME,
                            mappings=mappings)
