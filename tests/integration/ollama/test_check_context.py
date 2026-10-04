import os
from pathlib import Path

import httpx
import pytest

from paper_rag.core.embedders import get_embedder

text: str = (
    """X(6900) as a hadronic mediator of a gluonic dark-matter portalWe investigate X(6900) as a hadronic realization of a gluonic portal between a dark sector and QCD. The analysis is updated using the 2026 CMS observation of a family of all-charm structures and a recent combined LHCb–ATLAS–CMS analysis of the di-J/ψ spectrum. The CMS angular analysis favors <math altimg="si19.svg"><mrow><msup><mi>J</mi><mrow><mi>P</mi><mi>C</mi></mrow></msup><mo linebreak="goodbreak">=</mo><msup><mn>2</mn><mrow><mo>+</mo><mo>+</mo></mrow></msup></mrow></math>, motivating a spin-two mediator rather than the scalar ansatz used in earlier versions of this study. The combined analysis also demonstrates that the extracted X(6900) mass and width are significantly model dependent because of interference. We therefore use <math altimg="si20.svg"><mrow><msub><mi>M</mi><mi>X</mi></msub><mo linebreak="goodbreak">=</mo><mn>6.919</mn><mspace width="0.33em"/><mtext>GeV</mtext></mrow></math> and <math altimg="si21.svg"><mrow><msub><mstyle mathvariant="normal"><mi>Γ</mi></mstyle><mi>X</mi></msub><mo linebreak="goodbreak">=</mo><mn>70.3</mn><mspace width="0.33em"/><mtext>MeV</mtext></mrow></math> as a reference benchmark, corresponding to the narrow-width, weak-interference Model I of the combined analysis, while treating the spread among interference models as a systematic theoretical uncertainty. The interaction is<math altimg="si22.svg"><mrow><msub><mi mathvariant="script">L</mi><mrow><mrow><mi mathvariant="normal">i</mi></mrow><mi>n</mi><mi>t</mi></mrow></msub><mo linebreak="goodbreak">=</mo><mo>−</mo><mfrac><msub><mi>c</mi><mi>χ</mi></msub><mstyle mathvariant="normal"><mi>Λ</mi></mstyle></mfrac><msub><mi>X</mi><mrow><mi>μ</mi><mi>ν</mi></mrow></msub><msubsup><mi>T</mi><mi>χ</mi><mrow><mi>μ</mi><mi>ν</mi></mrow></msubsup><mo linebreak="goodbreak">−</mo><mfrac><msub><mi>c</mi><mi>g</mi></msub><mstyle mathvariant="normal"><mi>Λ</mi></mstyle></mfrac><msub><mi>X</mi><mrow><mi>μ</mi><mi>ν</mi></mrow></msub><msubsup><mi>T</mi><mi>g</mi><mrow><mi>μ</mi><mi>ν</mi></mrow></msubsup><mo>.</mo></mrow></math>Using the standard spin-two normalization,<math altimg="si23.svg"><mrow><mstyle mathvariant="normal"><mi>Γ</mi></mstyle><mrow><mo>(</mo><mi>X</mi><mo>→</mo><mi>g</mi><mi>g</mi><mo>)</mo></mrow><mo linebreak="goodbreak">=</mo><mfrac><mrow><msubsup><mi>c</mi><mi>g</mi><mn>2</mn></msubsup><msubsup><mi>M</mi><mi>X</mi><mn>3</mn></msubsup></mrow><mrow><mn>10</mn><mi>π</mi><msup><mstyle mathvariant="normal"><mi>Λ</mi></mstyle><mn>2</mn></msup></mrow></mfrac><mo>,</mo></mrow></math>and the gluonic gravitational form factor Ag(0), the leading spin-independent nucleon cross section is<math altimg="si24.svg"><mrow><msubsup><mi>σ</mi><mrow><mi>χ</mi><mi>N</mi></mrow><mrow><mrow><mi mathvariant="normal">S</mi></mrow><mi>I</mi></mrow></msubsup><mo linebreak="goodbreak">=</mo><mfrac><mrow><msubsup><mi>μ</mi><mrow><mi>χ</mi><mi>N</mi></mrow><mn>2</mn></msubsup><msubsup><mi>m</mi><mi>χ</mi><mn>2</mn></msubsup><msubsup><mi>m</mi><mi>N</mi><mn>2</mn></msubsup></mrow><mi>π</mi></mfrac><msup><mrow><mo stretchy="true">(</mo><mfrac><mrow><msub><mi>c</mi><mi>χ</mi></msub><msub><mi>c</mi><mi>g</mi></msub></mrow><mrow><msup><mstyle mathvariant="normal"><mi>Λ</mi></mstyle><mn>2</mn></msup><msubsup><mi>M</mi><mi>X</mi><mn>2</mn></msubsup></mrow></mfrac><mo stretchy="true">)</mo></mrow><mn>2</mn></msup><msub><mi>A</mi><mi>g</mi></msub><msup><mrow><mo>(</mo><mn>0</mn><mo>)</mo></mrow><mn>2</mn></msup><mo>.</mo></mrow></math>For <math altimg="si2.svg"><mrow><msub><mi>A</mi><mi>g</mi></msub><mrow><mo>(</mo><mn>0</mn><mo>)</mo></mrow><mo linebreak="goodbreak">=</mo><mn>0.42</mn></mrow></math>, <math altimg="si8.svg"><mrow><msub><mi>B</mi><mrow><mi>g</mi><mi>g</mi></mrow></msub><mo linebreak="goodbreak">=</mo><mn>0.10</mn></mrow></math>, and <math altimg="si25.svg"><mrow><msub><mi>m</mi><mi>χ</mi></msub><mo linebreak="goodbreak">=</mo><mn>100</mn><mspace width="0.33em"/><mtext>GeV</mtext></mrow></math>, the benchmark reference-scale estimate implies <math altimg="si26.svg"><mrow><msub><mi>c</mi><mi>χ</mi></msub><mo linebreak="goodbreak">/</mo><mstyle mathvariant="normal"><mi>Λ</mi></mstyle><mo>≲</mo><mn>1.87</mn><mo linebreak="goodbreak">×</mo><msup><mn>10</mn><mrow><mo>−</mo><mn>8</mn></mrow></msup><mspace width="0.33em"/><msup><mrow><mtext>GeV</mtext></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup></mrow></math> when the 90% C.L. XENONnT reference scale is imposed. The annihilation channel <math altimg="si4.svg"><mrow><mi>χ</mi><mover accent="true"><mi>χ</mi><mo>¯</mo></mover><mo>→</mo><msup><mi>X</mi><mo>*</mo></msup><mo>→</mo><mi>g</mi><mi>g</mi></mrow></math> is p-wave suppressed and resonantly enhanced at <math altimg="si27.svg"><mrow><msub><mi>m</mi><mi>χ</mi></msub><mo>≃</mo><msub><mi>M</mi><mi>X</mi></msub><mo linebreak="goodbreak">/</mo><mn>2</mn><mo linebreak="goodbreak">=</mo><mn>3.46</mn><mspace width="0.33em"/><mtext>GeV</mtext></mrow></math>. We show that the most important phenomenological uncertainty is no longer the existence of X(6900), which is now highly significant, but the interpretation of its line shape and hence the extraction of its mass, width, and gluonic coupling. We argue that a small set of numerical figures is essential for a publication-quality presentation: the direct-detection exclusion plane, the resonance line shape, and the resonant annihilation line shape."""
)


@pytest.fixture
def embedder():
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    try:
        httpx.get(f"{url}/api/tags", timeout=2).raise_for_status()
    except httpx.HTTPError:
        pytest.skip("Ollama n'est pas joignable")
    return get_embedder()


@pytest.mark.ollama
def test_embed_long_text_does_not_fail(embedder):
    long_text = "dark matter halo " * 1000  # environ 17 000 caractères
    vectors = embedder.embed([long_text])
    assert len(vectors) == 1
    assert len(vectors[0]) == embedder.dim


DATA = Path(__file__).parent / "data"


# @pytest.mark.ollama
# def test_embed_paper_with_mathml(embedder):
#     text = (DATA / "paper_311.txt").read_text(encoding="utf-8")
#     vectors = embedder.embed([text])
#     assert len(vectors[0]) == embedder.dim


import re


@pytest.mark.ollama
def test_embed_paper_without_markup(embedder):
    text = (DATA / "paper_311.txt").read_text(encoding="utf-8")
    cleaned = re.sub(r"<[^>]+>", "", text)
    print(cleaned)
    assert len(embedder.embed([cleaned])[0]) == embedder.dim
