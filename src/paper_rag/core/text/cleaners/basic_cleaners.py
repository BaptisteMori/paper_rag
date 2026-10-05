import html
import re

from paper_rag.core.text.cleaners.cleaner import TextCleaner


class NormalizeWhitespace(TextCleaner):
    def clean(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()


class UnescapeEntities(TextCleaner):
    def clean(self, text: str) -> str:
        return html.unescape(text)
