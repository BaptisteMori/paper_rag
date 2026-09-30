from pgvector.django import CosineDistance

from paper_rag.core.embedders import get_embedder
from paper_rag.core.model.models import PaperRecord as PaperRecordModel


def search(query: str, k: int = 5) -> list[tuple[PaperRecordModel, float]]:
    vector = get_embedder().embed_query(query)  # préfixe "search_query: " pour nomic
    papers = (
        PaperRecordModel.objects.exclude(embedding=None)
        .annotate(distance=CosineDistance("embedding", vector))
        .order_by("distance")[:k]
    )
    return [(p, 1 - p.distance) for p in papers]
