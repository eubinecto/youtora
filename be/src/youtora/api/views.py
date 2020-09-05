from typing import Optional

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from be.src.elastic.main import Search
from be.src.mongo.settings import CorporaDB
from be.src.youtora.api.errors import InvalidRequestError

app = Flask(__name__)
cors = CORS(app)


# handler for invalid request
@app.errorhandler(InvalidRequestError)
def handle_invalid_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/youtora_tracks/search')
@cross_origin()
def api_search_tracks():
    """
    api for searching tracks
    """
    params_dict = request.args
    # this is required
    content = params_dict.get('content', None)
    if not content:
        raise InvalidRequestError("parameter content is required, but not provided", 410)

    # these are optional
    chan_lang_code: Optional[str] = params_dict.get('chan_lang_code', None)
    caption_lang_code: Optional[str] = params_dict.get('caption_lang_code', None)
    views_boost: Optional[int] = params_dict.get('views_boost', None)
    like_ratio_boost: Optional[int] = params_dict.get('like_ratio_boost', None)
    subs_boost: Optional[int] = params_dict.get('subs_boost', None)
    from_: Optional[int] = params_dict.get('from', None)
    size: Optional[int] = params_dict.get('size', None)

    # build the parameters to pass
    search_params = {
        'content': content
    }
    if chan_lang_code:
        search_params['chan_lang_code'] = chan_lang_code
    if caption_lang_code:
        search_params['caption_lang_code'] = caption_lang_code
    if views_boost:
        search_params['views_boost'] = int(views_boost)
    if like_ratio_boost:
        search_params['like_ratio_boost'] = int(like_ratio_boost)
    if subs_boost:
        search_params['subs_boost'] = int(subs_boost)
    if from_:
        search_params['from_'] = int(from_)
    if size:
        search_params['size'] = int(size)

    results = Search.search_tracks(**search_params)
    return jsonify(results)


@app.route('youtora/dloaders/FrameDownloader/dl_frame')
@cross_origin()
def api_dl_frame():
    # get the arguments
    param_dict = request.args
    # required parameters
    vid_url = param_dict.get('vid_id', None)
    timestamp = param_dict.get('timestamp', None)
    # required check
    if None in (vid_url, timestamp):
        raise InvalidRequestError("Either vid_url or timestamp is not given. They are both required")

    # use the function to download the frame binary
    pass


@app.route("mongo/corpora_db/ml_gloss_raw_coll")
@cross_origin()
def api_ml_gloss_raw_coll():
    corpora_db = CorporaDB()
    results = list(corpora_db.ml_gloss_raw_coll.find())
    return jsonify(results)
