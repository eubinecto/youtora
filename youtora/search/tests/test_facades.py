# we are not accessing django's db, so just use unittest's one
from django.test import TestCase

from youtora.search.dataclasses import SrchQuery
from youtora.search.facades import SrchGeneralDoc


class SearchGeneralDocTestCase(TestCase):
    text = "hello"
    # queries to be used for testing
    is_auto_true = SrchQuery(text, is_auto=True)
    is_auto_false = SrchQuery(text, is_auto=False)

    # only the auto captions should be returned
    def test_add_filter_is_auto_true(self):
        srch_results = SrchGeneralDoc.exec(self.is_auto_true)
        self.assertTrue(len(srch_results) > 0)
        for srch_res in srch_results:
            self.assertEqual(True, srch_res.features['is_auto'])

    # only the manual captions should be returned
    def test_add_filter_is_auto_false(self):
        srch_results = SrchGeneralDoc.exec(self.is_auto_false)
        self.assertTrue(len(srch_results) > 0)
        for srch_res in srch_results:
            self.assertEqual(False, srch_res.features['is_auto'])
