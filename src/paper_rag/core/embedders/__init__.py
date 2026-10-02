from paper_rag.core.embedders.embedder import Embedder
from paper_rag.core.embedders.ollama_embedder import OllamaEmbedder
from paper_rag.core.utils.config import config

EMBEDDERS: dict[str, Embedder] = {"ollama": OllamaEmbedder}


def get_default_embedding_dim():
    cfg = config()["embedder"]
    return cfg["models"][cfg["default_model"]]["dim"]


def list_models(provider: str) -> list[str]:
    return list(config()["embedder"]["providers"][provider]["models"])


def get_embedder(provider: str | None = None, model: str | None = None) -> Embedder:
    cfg = config()["embedder"]
    provider = provider or cfg["default_provider"]
    model = model or cfg["default_model"]

    if provider not in EMBEDDERS:
        raise ValueError(f"Unknown provider '{provider}'. Available: {list(EMBEDDERS)}")
    provider_models = cfg["providers"][provider]["models"]
    if model not in provider_models:
        raise ValueError(
            f"Model '{model}' not available for '{provider}'. Available: {list(provider_models)}"
        )

    return EMBEDDERS[provider](
        model=provider_models[model],
        **cfg["models"][model],
    )
