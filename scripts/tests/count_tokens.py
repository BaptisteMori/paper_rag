import os
import re
import statistics

import httpx

import scripts._bootstrap  # noqa: F401
from paper_rag.core.model.models import PaperRecord

URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = "nomic-embed-text"  # à adapter si tu utilises un autre modèle


def count_tokens(client: httpx.Client, text: str) -> int | None:
    """Nombre de tokens vus par le modèle, ou None si ça dépasse le contexte."""
    resp = client.post(
        f"{URL}/api/embed",
        json={"model": MODEL, "input": text, "truncate": False},
    )
    if resp.status_code == 400 and "context length" in resp.text:
        return None
    resp.raise_for_status()
    return resp.json()["prompt_eval_count"]


abstracts = list(PaperRecord.objects.values_list("abstract", flat=True))

MATHML_TAGS = [
    "math",
    "mrow",
    "mi",
    "mo",
    "msup",
    "mn",
    "msub",
    "msubsup",
    "mfrac",
    "mstyle",
    "mtext",
    "mspace",
    "sup",
    "mover",
    "msqrt",
]
pattern = re.compile(r"</?(?:" + "|".join(MATHML_TAGS) + r")\b[^>]*>")

with httpx.Client(timeout=120) as client:
    counts = [
        (
            len(a),
            count_tokens(
                client,
                re.sub(pattern, "", a),
            ),
        )
        for a in abstracts
    ]

overflow = [c for c, t in counts if t is None]
ok = [(c, t) for c, t in counts if t is not None]

print(f"{len(abstracts)} abstracts, {len(overflow)} dépassent le contexte")
print(
    "tokens : médiane",
    statistics.median(t for _, t in ok),
    "| max",
    max(t for _, t in ok),
)
print("caractères/token (médiane) :", round(statistics.median(c / t for c, t in ok), 2))

worst = sorted(ok, key=lambda ct: ct[0] / ct[1])[:5]
for c, t in worst:
    print(c, "caractères,", t, "tokens, ratio", round(c / t, 2))
