from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField

from paper_rag.core.utils.config import config


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    embedding = VectorField(dimensions=config()["embedder"]["dim"], null=True)

    class Meta:
        db_table = "paper_records"
        constraints = [
            models.UniqueConstraint(fields=["source", "external_id"], name="uniq_source_paper")
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