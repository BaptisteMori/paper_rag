from django.db import models
from pgvector.django import HnswIndex, VectorField

from paper_rag.core.embedders import get_default_embedding_dim


class UpsertQuerySet(models.QuerySet):
    def upsert(self, objs, update_conflicts: bool = True):
        """
        INSERT ... ON CONFLICT DO UPDATE. Returned objects have their pk set (PostgreSQL).

        """
        model = self.model
        return self.bulk_create(
            objs,
            update_conflicts=update_conflicts,
            unique_fields=model.UNIQUE_FIELDS,
            update_fields=model.UPDATE_FIELDS,
        )


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UpsertQuerySet.as_manager()

    class Meta:
        abstract = True


class PaperRecord(BaseModel):
    source = models.CharField(max_length=32)
    external_id = models.CharField(max_length=64)
    title = models.TextField()
    abstract = models.TextField()
    authors = models.JSONField(default=list)
    published = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)
    embedding = VectorField(dimensions=get_default_embedding_dim(), null=True)
    record_hash = models.CharField(max_length=64, blank=True, default="")

    UNIQUE_FIELDS = ["source", "external_id"]
    UPDATE_FIELDS = [
        "title",
        "abstract",
        "authors",
        "published",
        "url",
        "embedding",
        "record_hash",
        "updated_at",
    ]

    class Meta:
        db_table = "paper_records"
        constraints = [
            models.UniqueConstraint(
                fields=["source", "external_id"], name="uniq_source_paper"
            )
        ]
        indexes = [
            HnswIndex(
                name="paper_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


class PaperRecordBaseEmbedding(BaseModel):
    # django add the "_id" automaticaly on FK
    paper = models.OneToOneField(
        PaperRecord, on_delete=models.DB_CASCADE, related_name="+"
    )  # models.DB_CASCADE -> delete on cascade postgres side
    text_hash = models.CharField(max_length=64)

    MODEL_NAME: str
    DIM: int

    UNIQUE_FIELDS = ["paper_id"]
    UPDATE_FIELDS = ["embedding", "text_hash", "updated_at"]

    class Meta:
        abstract = True


class NomicEmbedding(PaperRecordBaseEmbedding):

    MODEL_NAME = "nomic-embed-text"
    DIM = 768

    embedding = VectorField(dimensions=DIM)

    class Meta:
        db_table = "embedding_nomic_embed_text"
        indexes = [
            HnswIndex(
                name="emb_nomic_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


class BgeM3Embedding(PaperRecordBaseEmbedding):
    MODEL_NAME = "bge-m3"
    DIM = 1024
    embedding = VectorField(dimensions=DIM)

    class Meta:
        db_table = "embedding_bge_m3"
        indexes = [
            HnswIndex(
                name="emb_bge_m3_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


EMBEDDING_TABLES: dict[str, type[PaperRecordBaseEmbedding]] = {
    cls.MODEL_NAME: cls for cls in (NomicEmbedding, BgeM3Embedding)
}
