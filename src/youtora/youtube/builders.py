import logging
from typing import List

from src.youtora.youtube.errors import CaptionNotFoundError
from src.youtora.youtube.models import Video, Caption


class CaptionBuilder:
    # manually written captions, asr caption
    CAPTION_TYPES = ("manual", "auto")
    # the caption format I'll be using
    CAPTION_FORMAT = 'srv1'
    # list of caption formats used by youtube_dl
    FORMAT_IDX = {
        'srv1': 0,
        'srv2': 1,
        'srv3': 2,
        'ttml': 3,
        'vtt': 4
    }
    # korean, japanese, english, british english, french
    # we are only downloading captions of these languages .
    # these are the languages of the captions that I'll be collecting
    LANG_CODES_TO_COLLECT = ('ko', 'ja', 'en', 'en-GB', 'fr')

    def __init__(self, video: Video):
        self.manual_sub_info = video.manual_sub_info
        self.auto_sub_info = video.auto_sub_info
        self.vid_id = video.id

    def build_captions(self) -> List[Caption]:
        """
        :return:
        """
        logger = logging.getLogger("add_captions")
        # captions now should be a list of captions
        captions = list()
        # loop through all of the lang codes
        for lang_code in self.LANG_CODES_TO_COLLECT:
            try:
                # manual
                # first get all available manual captions.
                caption_type = "manual"
                manual_caption = self.build_caption(caption_type=caption_type,
                                                    lang_code=lang_code)
            except CaptionNotFoundError:
                # try getting an automatic one
                try:
                    caption_type = "auto"
                    auto_caption = self.build_caption(caption_type=caption_type,
                                                      lang_code=lang_code)
                except CaptionNotFoundError:
                    # automatic one was not found either
                    logger.warning("NOT FOUND: manual & auto:" + lang_code)
                else:
                    # collect the automatic caption
                    captions.append(auto_caption)
            else:
                # collect the manual caption
                captions.append(manual_caption)
        # return captions
        return captions

    def build_caption(self,
                      caption_type: str,
                      lang_code: str) -> Caption:
        """
        build the caption from video, with the given type & lang code.
        :param caption_type: manual = manually written, auto = ASR. the default is auto.
        :param lang_code: the language code should be given
        :return: a caption object
        """
        # input check - must be either  "manual" or "auto"
        if caption_type not in self.CAPTION_TYPES:
            raise ValueError(caption_type)
        # set the desired caption format in the CaptionScraper class.
        format_idx = self.FORMAT_IDX[self.CAPTION_FORMAT]
        # this is initially None
        caption_url = None
        # switch statement
        if caption_type == "manual":
            if lang_code in self.manual_sub_info:  # manual exists
                caption_url = self.manual_sub_info[lang_code][format_idx]['url']
        elif caption_type == "auto":  # auto exists
            if lang_code in self.auto_sub_info:
                caption_url = self.auto_sub_info[lang_code][format_idx]['url']

        if not caption_url:
            raise CaptionNotFoundError("NOT FOUND: {},{}"
                                       .format(caption_type, lang_code))
        # this will be the id of each caption
        caption_comp_key = "|".join([self.vid_id, caption_type, lang_code])
        # return the caption object with tracks
        caption = Caption(caption_id=caption_comp_key,
                          vid_id=self.vid_id,
                          url=caption_url)
        # return the caption
        return caption
