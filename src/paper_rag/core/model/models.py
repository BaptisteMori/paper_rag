from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField

from paper_rag.core.embedders import get_default_embedding_dim


class UpsertQuerySet(models.QuerySet):
    def upsert(self, objs, update_conflicts=True):
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

    UNIQUE_FIELDS = ["source", "external_id"]
    UPDATE_FIELDS = [
        "title",
        "abstract",
        "authors",
        "published",
        "url",
        "embedding",
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
