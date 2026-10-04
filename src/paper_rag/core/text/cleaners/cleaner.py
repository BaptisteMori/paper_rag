from abc import ABC, abstractmethod


class TextCleaner(ABC):
    """Just a text cleaner."""

    @abstractmethod
    def clean(self, text: str) -> str: ...


class CleaningPipeline(TextCleaner):
    """Apply text cleaner one by one."""

    def __init__(self, cleaners: list[TextCleaner]):
        self.cleaners = cleaners

    def clean(self, text: str) -> str:
        for cleaner in self.cleaners:
            text = cleaner.clean(text)
        return text
