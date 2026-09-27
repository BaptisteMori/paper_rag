import copy
import logging
import logging.config
from pathlib import Path
from typing import Any

from paper_rag.core.utils.config import config

_configured = False


def logger_config() -> dict[str, Any]:
    """Retourne la config logging du YAML, avec les chemins de fichiers résolus."""
    cfg = copy.deepcopy(config().get("logging", {}))
    for handler in cfg.get("handlers", {}).values():
        if filename := handler.get("filename"):
            path = Path(filename)
            path.parent.mkdir(
                parents=True, exist_ok=True
            )  # crée .build/logs/ si besoin
            handler["filename"] = str(path)
    return cfg


def load_logger_config() -> None:
    """Applique la configuration (une seule fois)."""
    global _configured
    if not _configured:
        logging.config.dictConfig(logger_config())
        _configured = True


def get_logger(name: str) -> logging.Logger:
    load_logger_config()
    return logging.getLogger(name)
