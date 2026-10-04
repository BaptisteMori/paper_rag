import re

from paper_rag.core.text.cleaners.cleaner import TextCleaner




class SpaceCleaner(TextCleaner):
    def clean(self, text: str) -> str:
        return re.sub(r"\s{2,}", " ", text)
