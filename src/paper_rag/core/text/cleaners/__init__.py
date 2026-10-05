from paper_rag.core.text.cleaners.basic_cleaners import (
    NormalizeWhitespace,
    UnescapeEntities,
)
from paper_rag.core.text.cleaners.cleaner import CleaningPipeline, TextCleaner
from paper_rag.core.text.cleaners.strip_markup import (
    StripMarkup,
    WhitelistedStripMarkup,
)
from paper_rag.core.utils.config import config

CLEANER_REGISTRY: dict[str, TextCleaner] = {
    "normalize_whitespace": NormalizeWhitespace,
    "unescape_entities": UnescapeEntities,
    "strip_markup": StripMarkup,
    "whitelisted_strip_markup": WhitelistedStripMarkup,
}


def get_default_cleaner_pipeline(cleaners: list[str] | None = None) -> CleaningPipeline:
    if not cleaners:
        cleaners = config()["text"]["cleaners"]["default_cleaning_pipeline"]

    initialized_cleaners: list[TextCleaner] = [CLEANER_REGISTRY[c]() for c in cleaners]

    return CleaningPipeline(initialized_cleaners)
