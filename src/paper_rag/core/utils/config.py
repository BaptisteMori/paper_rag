import os
import yaml
from pathlib import Path

CONFIG: dict[str:any] = {}


def load_config() -> None:
    config_file = Path(os.environ["CONFIG"]) / "config.yaml"
    with config_file.open("r", encoding="utf-8") as f:
        CONFIG.update(yaml.safe_load(f) or {})


def config() -> dict[str:any]:
    if CONFIG == {}:
        load_config()
    return CONFIG
