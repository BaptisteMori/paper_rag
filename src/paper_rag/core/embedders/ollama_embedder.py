import httpx
import os

from paper_rag.core.embedders.embedder import Embedder


class OllamaEmbedder(Embedder):
    """Uses Ollama's /api/embed endpoint (batch input)."""

    def __init__(
        self,
        model: str,
        dim: int,
        document_prefix: str = "",
        query_prefix: str = "",
        client: httpx.Client | None = None,
    ):
        self.model = model
        self.dim = dim
        self.document_prefix = document_prefix
        self.query_prefix = query_prefix
        self.url = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
        self.client = client or httpx.Client(timeout=120)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._call([self.document_prefix + t for t in texts])

    def embed_query(self, text: str) -> list[float]:
        prefix = "search_query: " if "nomic" in self.model else ""
        return self._call([prefix + text])[0]

    def _call(self, inputs: list[str]) -> list[list[float]]:
        resp = self.client.post(
            f"{self.url}/api/embed", json={"model": self.model, "input": inputs}
        )
        resp.raise_for_status()
        vectors = resp.json()["embeddings"]
        if vectors and len(vectors[0]) != self.dim:
            raise ValueError(
                f"Model returned dim {len(vectors[0])}, EMBEDDING_DIM is {self.dim}"
            )
        return vectors
