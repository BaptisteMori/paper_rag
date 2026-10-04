import re

from paper_rag.core.text.cleaners.cleaner import TextCleaner


class StripMarkup(TextCleaner):
    def clean(self, text: str) -> str:
        return re.sub(r"</?[A-Za-z][^>]*>", "", text)


class WhitelistedStripMarkup(TextCleaner):
    def __init__(self):
        self.MATHML_TAGS: list[str] = [
            "math",
            "mrow",
            "mi",
            "mo",
            "msup",
            "mn",
            "msub",
            "msubsup",
            "mfrac",
            "mstyle",
            "mtext",
            "mspace",
            "sup",
            "mover",
            "msqrt",
        ]
        self.pattern: re.Pattern[str] = re.compile(
            r"</?(?:" + "|".join(self.MATHML_TAGS) + r")\b[^>]*>"
        )

    def clean(self, text: str) -> str:
        return re.sub(self.pattern, "", text)
