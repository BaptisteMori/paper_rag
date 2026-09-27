from dataclasses import dataclass, field
from datetime import date

from paper_rag.core.business_object._business_object import BO


@dataclass
class PaperRecord(BO):

    source: str
    external_id: str
    title: str
    abstract: str
    authors: list[str] = field(default_factory=list)
    published: date | None = None
    url: str = ""

    def text_for_embedding(self) -> str:
        return f"{self.title}\n\n{self.abstract}"
