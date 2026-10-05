import re

from paper_rag.core.text.cleaners.cleaner import TextCleaner
from paper_rag.core.utils.config import config


class StripMarkup(TextCleaner):
    def clean(self, text: str) -> str:
        return re.sub(r"</?[A-Za-z][^>]*>", "", text)


class WhitelistedStripMarkup(TextCleaner):
    def __init__(self):
        self.mathml_tags: list[str] = config()["text"]["cleaners"]["mathml_tags"]
        self.pattern: re.Pattern[str] = re.compile(
            r"</?(?:" + "|".join(self.mathml_tags) + r")\b[^>]*>"
        )

    def clean(self, text: str) -> str:
        return re.sub(self.pattern, "", text)
