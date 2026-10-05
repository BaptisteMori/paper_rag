import pytest

from paper_rag.core.text.cleaners import (
    CleaningPipeline,
    NormalizeWhitespace,
    UnescapeEntities,
    WhitelistedStripMarkup,
)


def make_pipeline() -> CleaningPipeline:
    return CleaningPipeline(
        [WhitelistedStripMarkup(), UnescapeEntities(), NormalizeWhitespace()]
    )


def test_unescape_runs_after_strip_markup():
    text = "if  a &lt;mi&gt; <mi>x</mi>\n b"
    assert make_pipeline().clean(text) == "if a <mi> x b"


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("a  b\t c", id="whitespace"),
        pytest.param("x &lt; y", id="escaped_lt"),
        pytest.param('<mi mathvariant="script">x</mi> = 2', id="mathml"),
        pytest.param("plain text, nothing to clean", id="already_clean"),
    ],
)
def test_pipeline_is_idempotent(text):
    pipeline = make_pipeline()
    once = pipeline.clean(text)
    assert pipeline.clean(once) == once
