# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from youtora.search.builders import GeneralSrchQueryBuilder, GeneralResEntryBuilder
from youtora.search.facades import SrchFacade


def srch_general_doc(request) -> HttpResponse:
    # get the query parameter
    text = request.GET.get('text', None)
    # error handling
    if not text:
        return HttpResponseBadRequest(content="parameter required: text")
    params = {
        'text': text,
        'from_': 0,
        'size': 10,
    }
    # build a search query with the given params
    srch_q_builder = GeneralSrchQueryBuilder()
    srch_q_builder.prep(**params)
    res_e_builder = GeneralResEntryBuilder()
    # get the search results, using the facade class
    srch_res = SrchFacade(srch_q_builder, res_e_builder).exec()
    # serialise to json format
    return JsonResponse(data=srch_res.to_dict())
