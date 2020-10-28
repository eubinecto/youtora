from unittest import TestCase

from youtora.search.dataclasses import SrchQuery
from youtora.search.extractors import SrchResultsExtractor
from youtora.search.facades import SrchGeneralDoc


class SrchResultsExtractorTestCase(TestCase):
    text = "hello"
    # build a query to test with
    srch_query = SrchQuery(text)
    # search it on elastic search
    resp_dict = SrchGeneralDoc.build_and_exec(srch_query)
    # get the hits json
    hits_json = resp_dict['hits']['hits']

    def test_parse(self):
        srch_results = SrchResultsExtractor.parse(self.resp_dict)
        # now, what should this look like?
        for srch_res, hit_json in zip(srch_results, self.hits_json):
            # simple test
            self.assertEqual(srch_res.features, hit_json['_source']['caption'])
