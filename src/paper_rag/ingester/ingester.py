import logging

from paper_rag.ingester import SourceQuery, Source

from paper_rag.core.business_object.paper_record import PaperRecord
from paper_rag.core.model.models import PaperRecord as PaperRecordModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER: logging.Logger = logging.getLogger()


def ingest(source: Source, query: SourceQuery, limit: int) -> tuple[int, int]:
    created = updated = 0
    record: PaperRecord
    for record in source.fetch(query, limit):
        _, is_new = PaperRecordModel.objects.update_or_create(
            source=record.source,
            external_id=record.external_id,
            defaults={
                "title": record.title,
                "abstract": record.abstract,
                "authors": record.authors,
                "published": record.published,
                "url": record.url,
            },
        )
        created += is_new
        updated += not is_new
    LOGGER.info("Ingestion done: %d created, %d updated", created, updated)
    return created, updated
