from dataclasses import asdict, dataclass, fields
from typing import Any, Self


@dataclass
class BO:
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
