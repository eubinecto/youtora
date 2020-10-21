from django.test import TestCase

from youtora.collect.scrapers import IdiomRawScraper
from youtora.refine.extractors import IdiomExtractor


# warning:https://docs.djangoproject.com/en/3.1/topics/testing/overview/
# If your tests rely on database access such as creating or querying models,
# be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.


class IdiomExtractorTestCase(TestCase):
    # has 1 def
    catch_22_raw = IdiomRawScraper.scrape("Catch-22",
                                          "Catch-22",
                                          "https://en.wiktionary.org/wiki/Catch-22")
    # has 2 defs
    downing_street_raw = IdiomRawScraper.scrape("Downing_Street",
                                                "Downing Street",
                                                "https://en.wiktionary.org/wiki/Downing_Street")
    # has 6 defs
    dutch_oven_raw = IdiomRawScraper.scrape("Dutch_oven",
                                            "Dutch oven",
                                            "https://en.wiktionary.org/wiki/Dutch_oven")

    def test_parse_when_def_1(self):
        def_text = "A difficult situation from which there is no escape" \
                   " because it involves mutually conflicting or dependent conditions."
        def_context = "idiomatic"
        # parse the raw data
        catch_22 = IdiomExtractor.parse(self.catch_22_raw)
        catch_22.save()  # have to save this in order to access defs
        # assert equals meta data
        self.assertEqual(self.catch_22_raw.id, catch_22.id)
        self.assertEqual(self.catch_22_raw.idiom, catch_22.idiom)
        self.assertEqual(self.catch_22_raw.wiktionary_url, catch_22.wiktionary_url)
        # assert equals definition (there is only one for this case)
        self.assertEqual(def_text, catch_22.defs[0]['pure_text'])
        self.assertEqual(def_context, catch_22.defs[0]['context'])

    def test_parse_when_def_2(self):
        pure_text_1 = "a street leading off Whitehall in Westminster, London containing the residences of" \
                      " the Prime Minister and the Chancellor of the Exchequer"
        context_1 = None
        pure_text_2 = "the British government"
        context_2 = "idiomatic, by extension"
        downing_street = IdiomExtractor.parse(self.downing_street_raw)
        downing_street.save()  # have to save this in order to access defs
        # assert equals meta data
        self.assertEqual(self.downing_street_raw.id, downing_street.id)
        self.assertEqual(self.downing_street_raw.idiom, downing_street.idiom)
        self.assertEqual(self.downing_street_raw.wiktionary_url, downing_street.wiktionary_url)
        # assert equals definition (two definitions for this case)
        self.assertEqual(pure_text_1, downing_street.defs[0]['pure_text'])
        self.assertEqual(context_1, downing_street.defs[0]['context'])
        self.assertEqual(pure_text_2, downing_street.defs[1]['pure_text'])
        self.assertEqual(context_2, downing_street.defs[1]['context'])

    def test_parse_when_def_6(self):
        pure_text_1 = "A large metal cooking pot with a tight-fitting lid."
        pure_text_2 = "A portable oven consisting of a metal box, with shelves, placed before an open fire."
        pure_text_3 = "A protective cover for electrical contacts on a railway coupler, particularly but" \
                      " not exclusively used on the London Underground.[1]"
        pure_text_4 = "The situation where a person breaks wind under the bedcovers, sometimes pulling them" \
                      " over a bedmate's head as a prank."
        pure_text_5 = "A room or vehicle full of marijuana smoke."
        pure_text_6 = "The very end of a Dutch Masters cigar that has been rerolled" \
                      " with marijuana. This usage of the term is said to originate in New Brunswick, New Jersey.[2]"
        context_1 = None
        context_2 = None
        context_3 = "rail transport"
        context_4 = "slang"
        context_5 = None
        context_6 = None
        dutch_oven = IdiomExtractor.parse(self.dutch_oven_raw)
        dutch_oven.save()
        # assert equals meta info
        self.assertEqual(self.dutch_oven_raw.id, dutch_oven.id)
        self.assertEqual(self.dutch_oven_raw.idiom, dutch_oven.idiom)
        self.assertEqual(self.dutch_oven_raw.wiktionary_url, dutch_oven.wiktionary_url)
        # assert equals definitions
        self.assertEqual(pure_text_1, dutch_oven.defs[0]['pure_text'])
        self.assertEqual(pure_text_2, dutch_oven.defs[1]['pure_text'])
        self.assertEqual(pure_text_3, dutch_oven.defs[2]['pure_text'])
        self.assertEqual(pure_text_4, dutch_oven.defs[3]['pure_text'])
        self.assertEqual(pure_text_5, dutch_oven.defs[4]['pure_text'])
        self.assertEqual(pure_text_6, dutch_oven.defs[5]['pure_text'])
        # assert equals contexts
        self.assertEqual(context_1, dutch_oven.defs[0]['context'])
        self.assertEqual(context_2, dutch_oven.defs[1]['context'])
        self.assertEqual(context_3, dutch_oven.defs[2]['context'])
        self.assertEqual(context_4, dutch_oven.defs[3]['context'])
        self.assertEqual(context_5, dutch_oven.defs[4]['context'])
        self.assertEqual(context_6, dutch_oven.defs[5]['context'])
        # check if filter works properly
        self.assertEqual(6, len(dutch_oven.defs))
