import re
from collections import Counter

import scripts._bootstrap  # noqa: F401
from paper_rag.core.model.models import PaperRecord

abstracts = list(PaperRecord.objects.values_list("abstract", flat=True))
cmds = Counter()
lenghts = []
tags = Counter()
pattern = re.compile(r"</?([A-Za-z][A-Za-z0-9]*)")
GENERAL = re.compile(r"</?[A-Za-z][^>]*>")
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
SPECIFIC = re.compile(r"</?(?:" + "|".join(MATHML_TAGS) + r")\b[^>]*>")
print(SPECIFIC)
for a in abstracts:
    cmds.update(re.findall(r"\\[a-zA-Z]+", a))
    lenghts.append(len(a))
    # if "\\mathcal" in a or "\\rm" in a:
    #     print(a)
    # if len(a) in (4564, 5358, 3310):  # les plus longs
    #     print(
    #         len(a),
    #         "balises:",
    #         len(re.findall(r"</?[A-Za-z][^>]*>", a)),
    #         "latex:",
    #         len(re.findall(r"\\[a-zA-Z]+", a)),
    #     )
    tags.update(re.findall(r"</?([A-Za-z][A-Za-z0-9]*)", a))
    # for m in pattern.finditer(a):
    #     if m.group(1) == "E":
    #         print(repr(a[max(0, m.start() - 40) : m.end() + 60]))
    g = GENERAL.sub("", a)
    s = SPECIFIC.sub("", a)
    if g != s:
        print("DIFFÉRENCE sur un abstract de", len(a), "caractères")

lenghts.sort(reverse=True)
print(lenghts[:20])

print(len(abstracts), "abstracts")
print(cmds.most_common(10))
print(tags.most_common())
