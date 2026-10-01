from dataclasses import dataclass
from pgvector.django import CosineDistance

from paper_rag.core.embedders import get_embedder

from paper_rag.core.model.models import EMBEDDING_TABLES
from paper_rag.core.model.models import PaperRecord as PaperRecordModel


@dataclass
class SearchHit:
    paper: PaperRecordModel
    score: float


def hit_to_dict(hit: SearchHit) -> dict:
    p = hit.paper
    return {
        "id": p.pk,
        "source": p.source,
        "external_id": p.external_id,
        "title": p.title,
        "abstract": p.abstract,
        "authors": p.authors,
        "published": p.published.isoformat() if p.published else None,
        "url": p.url,
        "score": round(hit.score, 4),
    }


def search(query, k: int = 5, provider: str | None = None, model: str | None = None):
    embedder = get_embedder(provider, model)
    table = EMBEDDING_TABLES[embedder.model]

    vector = embedder.embed_query(query)
    rows = (
        table.objects.select_related("paper")
        .annotate(distance=CosineDistance("embedding", vector))
        .order_by("distance")[:k]
    )
    return [SearchHit(paper=row.paper, score=1 - row.distance) for row in rows]
