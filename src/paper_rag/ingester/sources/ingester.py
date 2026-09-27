from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field

from paper_rag.core.business_object.paper_record import PaperRecord
from paper_rag.core.utils.dates import date


@dataclass
class SourceQuery:
    """Each sources have it's own query format, but document have common fields"""

    text: str | None = None
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    since: date | None = None
    until: date | None = None
    raw: str | None = None


class Source(ABC):
    """A provider of scientific papers (INSPIRE, arXiv, OpenAlex...)."""

    name: str

    @abstractmethod
    def fetch(self, query: SourceQuery, limit: int = 100) -> Iterator[PaperRecord]:
        """Yield papers matching `query`, at most `limit`."""
