# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from youtora.search.dataclasses import SrchQuery
from youtora.search.facades import SrchGeneralIdx


def srch_general_doc(request) -> HttpResponse:
    # get the query parameter
    text = request.GET.get('text', None)
    # error handling
    if not text:
        return HttpResponseBadRequest(content="parameter required: text")
    # build a query
    srch_query = SrchQuery(text)
    # get the search results, using the facade class
    srch_results = SrchGeneralIdx.exec(srch_query)
    # serialise to json format
    srch_results_json = [srch_res.to_dict() for srch_res in srch_results]
    # return as a json response
    data = {
        'results': srch_results_json,
        'meta': None
    }
    return JsonResponse(data=data)
