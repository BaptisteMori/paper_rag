from abc import ABC, abstractmethod


class Embedder(ABC):
    """Turns text into fixed-size vectors."""

    dim: int

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed documents (batch)."""

    def embed_query(self, text: str) -> list[float]:
        """Embed a search query. Override when the model needs a query prefix."""
        return self.embed([text])[0]
