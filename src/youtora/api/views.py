from typing import Optional

from flask import Flask, request, jsonify

from src.elastic.main import Search
from src.youtora.api.errors import InvalidRequestError

app = Flask(__name__)


# handler for invalid request
@app.errorhandler(InvalidRequestError)
def handle_invalid_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/youtora_tracks/search')
def api_search_tracks():
    """
    api for searching tracks
    """
    params_dict = request.args
    # this is required
    try:
        content = params_dict['content']
    except KeyError:
        raise InvalidRequestError("parameter content is required, but not provided", 410)
    else:
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

