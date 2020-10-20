from django.test import TestCase
# from unittest import TestCase
from youtora.collect.models import IdiomRaw
from youtora.collect.scrapers import IdiomRawScraper
from youtora.refine.extractors import IdiomExtractor
# warning:https://docs.djangoproject.com/en/3.1/topics/testing/overview/
# If your tests rely on database access such as creating or querying models,
# be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.


class IdiomExtractorTestCase(TestCase):

    def setUp(self) -> None:
        """
        get raw idioms from the db, containing different number of idioms
        :return:
        """
        # has 1 def
        self.catch_22_raw = IdiomRawScraper.scrape("Catch-22",
                                                   "Catch-22",
                                                   "https://en.wiktionary.org/wiki/Catch-22")
        # has 2 defs
        self.downing_street_raw = IdiomRawScraper.scrape("Downing_Street",
                                                         "Downing Street",
                                                         "https://en.wiktionary.org/wiki/Downing_Street")
        # has 6 defs
        self.dutch_oven_raw = IdiomRawScraper.scrape("Dutch_oven",
                                                     "Dutch oven",
                                                     "https://en.wiktionary.org/wiki/Dutch_oven")

    def test_parse_when_def_1(self):
        def_text = "A difficult situation from which there is no escape" \
                   " because it involves mutually conflicting or dependent conditions."
        def_context = "idiomatic"
        # parse the raw data
        catch_22 = IdiomExtractor.parse(self.catch_22_raw)
        catch_22.save()  # have to save this in order to test with it
        # assert equals meta data
        self.assertEqual(self.catch_22_raw.id, catch_22.id)
        self.assertEqual(self.catch_22_raw.idiom, catch_22.idiom)
        self.assertEqual(self.catch_22_raw.wiktionary_url, catch_22.wiktionary_url)
        # assert equals definition (there is only one for this case)
        self.assertEqual(def_text, catch_22.defs[0].pure_text)
        self.assertEqual(def_context, catch_22.defs[0].context)

    def test_parse_when_def_2(self):
        pure_text_1 = "a street leading off Whitehall in Westminster, London containing the residences of" \
                      " the Prime Minister and the Chancellor of the Exchequer"
        context_1 = None
        pure_text_2 = "the British government"
        context_2 = "idiomatic, by extension"
        downing_street = IdiomExtractor.parse(self.downing_street_raw)
        # assert equals meta data
        self.assertEqual(self.downing_street_raw.id, downing_street.id)
        self.assertEqual(self.downing_street_raw.idiom, downing_street.idiom)
        self.assertEqual(self.downing_street_raw.wiktionary_url, downing_street.wiktionary_url)
        # assert equals definition (two definitions for this case)
        self.assertEqual(pure_text_1, downing_street.defs[0].pure_text)
        self.assertEqual(context_1, downing_street.defs[0].context)
        self.assertEqual(pure_text_2, downing_street.defs[1].pure_text)
        self.assertEqual(context_2, downing_street.defs[1].context)

    def test_parse_when_def_6(self):
        # idiom = IdiomExtractor.parse(self.dutch_oven_raw_6)
        # # assert equals meta info
        # self.assertEqual(self.dutch_oven_raw_6.id, idiom.id)
        # self.assertEqual(self.dutch_oven_raw_6.idiom, idiom.idiom)
        # self.assertEqual(self.dutch_oven_raw_6.wiktionary_url, idiom.wiktionary_url)
        # # assert equals definitions
        # self.assertEqual()
        pass



