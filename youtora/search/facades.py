class SearchGeneralDoc:
    """
    facade class for searching general_doc.
    """

    @classmethod
    def run(cls, text: str,
            capt_lang_code: str = None, chan_lang_code: str = None,
            views_boost: int = 10, subs_boost: int = 10):
        """
        searches the general doc
        :param text: the text to search for
        :param capt_lang_code:  lang_code constraint for captions
        :param chan_lang_code: lang_code constraint for channel
        :param views_boost:
        :param subs_boost:
        :return:
        """
        pass
