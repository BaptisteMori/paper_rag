import logging
from itertools import batched

from django.db import transaction

from paper_rag.core.business_object.paper_record import PaperRecord
from paper_rag.core.embedders.embedder import Embedder
from paper_rag.core.model.models import EMBEDDING_TABLES, PaperRecordBaseEmbedding
from paper_rag.core.model.models import PaperRecord as PaperRecordModel
from paper_rag.core.text.cleaners import (
    CleaningPipeline,
    NormalizeWhitespace,
    TextCleaner,
    WhitelistedStripMarkup,
)
from paper_rag.core.utils.hash import hash_strings
from paper_rag.ingester import Source, SourceQuery

LOGGER = logging.getLogger(__name__)

Key = tuple[str, str]  # (source, external_id)


def _key(record: PaperRecord) -> Key:
    return (record.source, record.external_id)


def _deduplicate(records: tuple[PaperRecord, ...]) -> list[PaperRecord]:
    return list({_key(r): r for r in records}.values())


def _upsert_embeddings(
    records: list[PaperRecord],
    paper_ids: dict[Key, int],
    table: type[PaperRecordBaseEmbedding],
    embedder: Embedder,
    cleaners: CleaningPipeline | None = None,
) -> int:
    """
    Compute and store embeddings only for papers whose text (or model) changed.

    Args:
      reorcds: A list of PaperRecord.
      table: the table where to save the embeddings
      embedder: the provider configured with the model of embedding
      cleaners: A pipeline configured with the cleaners,
        to clean the text before hashing and embedding

    Returns:
      The new minimum port.
    """
    if not cleaners:
        cleaners = CleaningPipeline()
    # (paper_id, hash, texte) for each article
    candidates: list = []
    for record in records:
        cleaned_text: str = cleaners.clean(record.text_for_embedding())
        candidates.append(
            (
                paper_ids[_key(record)],
                hash_strings([embedder.model, cleaned_text]),
                cleaned_text,
            )
        )

    # Get the hashs of the paper_id
    stored = dict(
        table.objects.filter(
            paper_id__in=[pid for pid, _, _ in candidates]
        ).values_list("paper_id", "text_hash")
    )
    pending = [(pid, h, text) for pid, h, text in candidates if stored.get(pid) != h]
    if not pending:
        return 0

    # vectors = embedder.embed([text for _, _, text in pending])
    try:
        vectors = embedder.embed([text for _, _, text in pending])
    except RuntimeError:
        for pid, _, text in pending:
            try:
                embedder.embed([text])
            except RuntimeError as e:
                LOGGER.error("Paper %s failed (%d chars): %s", pid, len(text), e)
        raise

    table.objects.upsert(
        [
            table(paper_id=pid, text_hash=h, embedding=vector)
            for (pid, h, _), vector in zip(pending, vectors, strict=True)
        ]
    )
    return len(pending)


@transaction.atomic
def _upsert_papers(records: list[PaperRecord]) -> dict[Key, int]:
    """Upsert the papers and return their database ids."""
    rows: list[PaperRecordModel] = PaperRecordModel.objects.upsert(
        [PaperRecordModel(**r.to_dict()) for r in records]
    )
    return {(row.source, row.external_id): row.pk for row in rows}


def ingest(
    source: Source,
    query: SourceQuery,
    limit: int,
    embedder: Embedder,
    batch_size: int = 32,
    cleaning_pipeline: CleaningPipeline | None = None,
) -> tuple[int, int]:
    """Fetch papers, upsert them, then (re)compute only the embeddings whose text changed.
    Returns (papers upserted, embeddings computed)."""
    table = EMBEDDING_TABLES[embedder.model]
    nb_papers = nb_embedded = 0

    # setup text cleaners
    if not cleaning_pipeline:
        cleaners: list[TextCleaner] = [WhitelistedStripMarkup(), NormalizeWhitespace()]
        cleaning_pipeline: CleaningPipeline = CleaningPipeline(cleaners)

    for chunk in batched(source.fetch(query, limit), batch_size):
        records = _deduplicate(chunk)

        paper_ids = _upsert_papers(records)
        nb_embedded += _upsert_embeddings(
            records, paper_ids, table, embedder, cleaning_pipeline
        )
        nb_papers += len(records)

        LOGGER.info(
            "%d/%d (max limit) papers processed, %d embeddings computed",
            nb_papers,
            limit,
            nb_embedded,
        )

    return nb_papers, nb_embedded
