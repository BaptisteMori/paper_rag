from datetime import date

import pytest

from paper_rag.core.utils.dates import parse_date


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2024-03-15", date(2024, 3, 15)),
        ("2024-03", date(2024, 3, 1)),  # Missing Day -> 1st
        ("2024", date(2024, 1, 1)),  # Missing month -> 01
        (None, None),
        ("", None),
        ("2024-13-01", None),  # Invalid month
    ],
)
def test_parse_date(value, expected):
    assert parse_date(value) == expected
