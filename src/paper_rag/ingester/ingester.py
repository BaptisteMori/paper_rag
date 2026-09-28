from itertools import batched
import logging

from paper_rag.core.embedders import get_embedder, Embedder

from paper_rag.ingester import SourceQuery, Source

from paper_rag.core.business_object.paper_record import PaperRecord
from paper_rag.core.model.models import PaperRecord as PaperRecordModel
from paper_rag.core.utils.config import config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER: logging.Logger = logging.getLogger()


def ingest(
    source: Source, query: SourceQuery, limit: int, batch_size: int = 100
) -> int:
    pushed = 0

    embedder: Embedder = get_embedder(provider=config()["embedder"]["default_provider"])

    rows: list[PaperRecordModel] = []
    vectors: list[list[float]] = []
    records: list[PaperRecord]
    r: PaperRecord
    for records in batched(source.fetch(query, limit), batch_size):
        vectors = embedder.embed(texts=[r.text_for_embedding() for r in records])
        LOGGER.info(f"Embedded {len(records)} records")
        rows = [
            PaperRecordModel(**r.to_dict(), embedding=v)
            for r, v in zip(records, vectors, strict=True)
        ]

        PaperRecordModel.objects.upsert(
            rows,
            update_conflicts=True,
        )
        pushed += len(rows)
    return pushed
