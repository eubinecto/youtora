import re
from typing import List, Generator, Optional
from .models import MLGloss, MLGlossRaw, MLGlossDesc
from bs4 import BeautifulSoup


class MLGlossRawParser:
    """
    houses logic for parsing raw MLGloss
    """
    # format with the file name of the svg file
    IMAGES_ENDPOINT = "https://developers.google.com/machine-learning/glossary/images/"
    # note: .* does not match new line.
    TOPIC_SENT_REGEXP = re.compile(r"^[\s\S]*?[.|:]")
    IMG_SRC_REGEXP = re.compile(r"/machine-learning/glossary/images/")
    CATEGORY_REGEXP = re.compile(r"<div class=\"glossary-icon\" title=\"(.*)\">.*</div>")

    @classmethod
    def parse(cls) -> List[MLGloss]:
        # get MlGlossRaw data
        ml_gloss_raw_coll = ...
        ml_gloss_raws: Generator[MLGlossRaw, None, None] = (
            MLGlossRaw(id=res['_id'],
                       word=res['word'],
                       credit=res['credit'],
                       desc_raw=res['desc_raw'],
                       category_raw=res['category_raw'])
            for res in ml_gloss_raw_coll.find()
        )  # ml_gloss_raws generator
        # parse it into ml glosses
        ml_glosses: List[MLGloss] = [
            MLGloss(id="ml_gloss|" + ml_gloss_raw.id.split("|")[-1],
                    word=ml_gloss_raw.word,
                    credit=ml_gloss_raw.credit,
                    desc=cls._parse_desc_raw(ml_gloss_raw.desc_raw),
                    category=cls._parse_category_raw(ml_gloss_raw.category_raw))
            for ml_gloss_raw in ml_gloss_raws
        ]
        # return it
        return ml_glosses

    @classmethod
    def _parse_desc_raw(cls, desc_raw: str) -> MLGlossDesc:
        desc_raw = cls.IMG_SRC_REGEXP.sub(repl=cls.IMAGES_ENDPOINT, string=desc_raw)
        desc_raw_bs = BeautifulSoup(desc_raw, 'html.parser')
        pure_text = desc_raw_bs.get_text().strip()
        topic_sent = cls.TOPIC_SENT_REGEXP.findall(string=pure_text)[0]
        return MLGlossDesc(topic_sent=topic_sent,
                           pure_text=pure_text,
                           desc_raw=desc_raw)

    @classmethod
    def _parse_category_raw(cls, category_raw: Optional[str]) -> Optional[str]:
        """
        category raw may not exist.
        e.g. <div class="glossary-icon" title="Sequence Models">#seq</div>
        """
        if category_raw:
            return cls.CATEGORY_REGEXP.findall(category_raw)[0]
        return None
