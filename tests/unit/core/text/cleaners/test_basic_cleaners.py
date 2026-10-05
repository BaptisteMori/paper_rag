import pytest

from paper_rag.core.text.cleaners.basic_cleaners import NormalizeWhitespace


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("a b", "a b", id="already_clean"),
        pytest.param("a    b", "a b", id="multiple_spaces"),
        pytest.param("a\tb", "a b", id="single_tab"),
        pytest.param("a\nb", "a b", id="single_newline"),
        pytest.param("a\n\nb", "a b", id="blank_line"),
        pytest.param("a \t\n b", "a b", id="mixed_whitespace"),
        pytest.param("  a  ", "a", id="leading_trailing"),
        pytest.param("a\u00a0b", "a b", id="non_breaking_space"),
        pytest.param("", "", id="empty"),
        pytest.param(" \t\n ", "", id="only_whitespace"),
    ],
)
def test_space_cleaner(value, expected):
    assert NormalizeWhitespace().clean(value) == expected
