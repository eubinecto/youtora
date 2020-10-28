# we are not accessing django's db, so just use unittest's one
from unittest import TestCase

from youtora.search.dataclasses import SearchQuery
from youtora.search.facades import SearchGeneralDoc


class SearchGeneralDocTestCase(TestCase):
    text = "hello"
    # queries to be used for testing
    is_auto_true = SearchQuery(text, is_auto=True)
    is_auto_false = SearchQuery(text, is_auto=False)

    # only the auto captions should be returned
    def test_add_filter_is_auto_true(self):
        res = SearchGeneralDoc.exec(self.is_auto_true)
        self.assertTrue(len(res['hits']['hits']) > 0)
        for hit in res['hits']['hits']:
            src = hit['_source']
            self.assertEqual(True, src['caption']['is_auto'])

    # only the manual captions should be returned
    def test_add_filter_is_auto_false(self):
        res = SearchGeneralDoc.exec(self.is_auto_false)
        self.assertTrue(len(res['hits']['hits']) > 0)
        for hit in res['hits']['hits']:
            src = hit['_source']
            self.assertEqual(False, src['caption']['is_auto'])
