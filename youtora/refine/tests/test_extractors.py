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

    # has 0 defs
    chr_pres_raw = IdiomRawScraper.scrape("Christmas_present",
                                          "Christmas present",
                                          "https://en.wiktionary.org/wiki/Christmas_present")

    # big picture: having error with this, don't know why. have to debug.
    # def_text = cls.TEXT_NO_CONTEXT_RE.findall(list_text)[0]
    # IndexError: list index out of range
    big_picture_raw = IdiomRawScraper.scrape("big_picture",
                                             "big picture",
                                             "https://en.wiktionary.org/wiki/big_picture")

    def test_parse_when_set_1_def_1(self):
        def_text = "A difficult situation from which there is no escape" \
                   " because it involves mutually conflicting or dependent conditions."
        def_context = "idiomatic"
        # parse the raw data
        catch_22 = IdiomExtractor.parse(self.catch_22_raw)
        catch_22.save()  # have to save this in order to access defs
        # assert equals definition (there is only one for this case)
        self.assertEqual(def_text, catch_22.def_sets[0]['defs'][0]['text'])
        self.assertEqual(def_context, catch_22.def_sets[0]['defs'][0]['context'])

    def test_parse_when_set_1_def_2(self):
        def_text_1 = "a street leading off Whitehall in Westminster, London containing the residences of" \
                     " the Prime Minister and the Chancellor of the Exchequer"
        def_text_2 = "the British government"
        def_context_1 = None
        def_context_2 = "idiomatic, by extension"
        downing_street = IdiomExtractor.parse(self.downing_street_raw)
        downing_street.save()  # have to save this in order to access defs
        # assert equals definition (two definitions for this case)
        self.assertEqual(def_text_1, downing_street.def_sets[0]['defs'][0]['text'])
        self.assertEqual(def_context_1, downing_street.def_sets[0]['defs'][0]['context'])
        self.assertEqual(def_text_2, downing_street.def_sets[0]['defs'][1]['text'])
        self.assertEqual(def_context_2, downing_street.def_sets[0]['defs'][1]['context'])

    def test_parse_when_set_1_def_6(self):
        def_text_1 = "A large metal cooking pot with a tight-fitting lid."
        def_text_2 = "A portable oven consisting of a metal box, with shelves, placed before an open fire."
        def_text_3 = "A protective cover for electrical contacts on a railway coupler, particularly but" \
                     " not exclusively used on the London Underground.[1]"
        def_text_4 = "The situation where a person breaks wind under the bedcovers, sometimes pulling them" \
                     " over a bedmate's head as a prank."
        def_text_5 = "A room or vehicle full of marijuana smoke."
        def_text_6 = "The very end of a Dutch Masters cigar that has been rerolled" \
                     " with marijuana. This usage of the term is said to originate in New Brunswick, New Jersey.[2]"
        def_text_7 = "Used other than with a figurative or idiomatic meaning: see Dutch,‎ oven."
        context_1 = None
        context_2 = None
        context_3 = "rail transport"
        context_4 = "slang"
        context_5 = None
        context_6 = None
        context_7 = None
        dutch_oven = IdiomExtractor.parse(self.dutch_oven_raw)
        dutch_oven.save()
        # assert equals meta info
        self.assertEqual(self.dutch_oven_raw.id, dutch_oven.id)
        self.assertEqual(self.dutch_oven_raw.text, dutch_oven.text)
        self.assertEqual(self.dutch_oven_raw.wiktionary_url, dutch_oven.wiktionary_url)
        # assert equals definitions
        self.assertEqual(def_text_1, dutch_oven.def_sets[0]['defs'][0]['text'])
        self.assertEqual(def_text_2, dutch_oven.def_sets[0]['defs'][1]['text'])
        self.assertEqual(def_text_3, dutch_oven.def_sets[0]['defs'][2]['text'])
        self.assertEqual(def_text_4, dutch_oven.def_sets[0]['defs'][3]['text'])
        self.assertEqual(def_text_5, dutch_oven.def_sets[0]['defs'][4]['text'])
        self.assertEqual(def_text_6, dutch_oven.def_sets[0]['defs'][5]['text'])
        self.assertEqual(def_text_7, dutch_oven.def_sets[0]['defs'][6]['text'])

        # assert equals contexts
        self.assertEqual(context_1, dutch_oven.def_sets[0]['defs'][0]['context'])
        self.assertEqual(context_2, dutch_oven.def_sets[0]['defs'][1]['context'])
        self.assertEqual(context_3, dutch_oven.def_sets[0]['defs'][2]['context'])
        self.assertEqual(context_4, dutch_oven.def_sets[0]['defs'][3]['context'])
        self.assertEqual(context_5, dutch_oven.def_sets[0]['defs'][4]['context'])
        self.assertEqual(context_6, dutch_oven.def_sets[0]['defs'][5]['context'])
        self.assertEqual(context_7, dutch_oven.def_sets[0]['defs'][6]['context'])

        # check if filter works properly
        self.assertEqual(7, len(dutch_oven.def_sets[0]['defs']))

    def test_parse_when_set_2(self):
        pass

    def test_parse_when_big_picture(self):
        """
        what's wrong with this one?
        :return:
        """
        def_text_1 = "The totality of a situation."
        def_text_2 = "The main film in a double feature."
        def_context_1 = None
        def_context_2 = "Britain, dated"
        big_picture = IdiomExtractor.parse(self.big_picture_raw)
        big_picture.save()

        self.assertEqual(def_text_1, big_picture.def_sets[0]['text'])
        self.assertEqual(def_context_1, big_picture.def_sets[0]['context'])
        self.assertEqual(def_text_2, big_picture.def_sets[1]['text'])
        self.assertEqual(def_context_2, big_picture.def_sets[1]['context'])

    def test_ext_ol_def_list(self):
        ol_def_list = IdiomExtractor._ext_ol_defs(self.chr_pres_raw.main_html)
        self.assertTrue(len(ol_def_list) == 2)

    def test_ext_pos(self):
        ol_def_list = IdiomExtractor._ext_ol_defs(self.chr_pres_raw.main_html)
        pos_list = [IdiomExtractor._ext_pos(ol_def) for ol_def in ol_def_list]
        self.assertEqual("Noun", pos_list[0])
        self.assertEqual("Noun", pos_list[1])
