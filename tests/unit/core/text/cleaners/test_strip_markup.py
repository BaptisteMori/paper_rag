import pytest

from paper_rag.core.text.cleaners.strip_markup import (
    StripMarkup,
    WhitelistedStripMarkup,
)

CASES = [
    {
        "id": "mathml_complex",
        "value": (
            "of the di-J/ψ spectrum. The CMS angular analysis favors "
            '<math altimg="si19.svg"><mrow><msup><mi>J</mi>'
            "<mrow><mi>P</mi><mi>C</mi></mrow></msup>"
            '<mo linebreak="goodbreak">=</mo><msup><mn>2</mn>'
            "<mrow><mo>+</mo><mo>+</mo></mrow></msup></mrow></math>, "
            "motivating a spin-two mediator rather than the scalar ansatz "
            "used in earlier versions of this study."
        ),
        "expected_StripMarkup": (
            "of the di-J/ψ spectrum. The CMS angular analysis favors "
            "JPC=2++, motivating a spin-two mediator rather than the scalar "
            "ansatz used in earlier versions of this study."
        ),
        "expected_WhitelistedStripMarkup": (
            "of the di-J/ψ spectrum. The CMS angular analysis favors "
            "JPC=2++, motivating a spin-two mediator rather than the scalar "
            "ansatz used in earlier versions of this study."
        ),
    },
    {
        "id": "mathml_simple",
        "value": '<mi mathvariant="script">x</mi>',
        "expected_StripMarkup": "x",
        "expected_WhitelistedStripMarkup": "x",
    },
    {
        "id": "lone_lt_gt_in_text",
        "value": "a < b and c > d",
        "expected_StripMarkup": "a < b and c > d",
        "expected_WhitelistedStripMarkup": "a < b and c > d",
    },
    {
        "id": "comparison_operators",
        "value": "E<5 GeV and p>2",
        "expected_StripMarkup": "E<5 GeV and p>2",
        "expected_WhitelistedStripMarkup": "E<5 GeV and p>2",
    },
    {
        "id": "lone_lt_gt_between_words",
        "value": "x<y and z>w",
        "expected_StripMarkup": "xw",  # <= here, strip to general
        "expected_WhitelistedStripMarkup": "x<y and z>w",
    },
    {
        "id": "latex_with_lt_gt_and_markup",
        "value": (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of> inelasti"
        ),
        "expected_StripMarkup": (
            "on zero. A dedicated LZ search over " "$271 inelasti"
        ),  # <= here, strip to general
        "expected_WhitelistedStripMarkup": (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of> inelasti"
        ),
    },
    {
        "id": "latex_with_lt_gt_without_markup",
        "value": (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti"
        ),
        "expected_StripMarkup": (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti"
        ),
        "expected_WhitelistedStripMarkup": (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti"
        ),
    },
    {
        "id": "mspace",
        "value": "test <mspace width='1em'/> test",
        "expected_StripMarkup": "test  test",  # <= limit, keep the multiple space
        "expected_WhitelistedStripMarkup": "test  test",  # <= limit, keep the multiple space
    },
    {
        "id": "unknown_markup",
        "value": "<mouse>x</mouse>",
        "expected_StripMarkup": "x",
        "expected_WhitelistedStripMarkup": "<mouse>x</mouse>",  # <= limit,
        # don't delete unknown markup
    },
    {
        "id": "closing_tag_with_space",
        "value": "</mi > test",
        "expected_StripMarkup": " test",
        "expected_WhitelistedStripMarkup": " test",
    },
    {
        "id": "empty",
        "value": "",
        "expected_StripMarkup": "",
        "expected_WhitelistedStripMarkup": "",
    },
]


def cases_for(key: str):
    return [pytest.param(c["value"], c[key], id=c["id"]) for c in CASES]


@pytest.mark.parametrize(("value", "expected"), cases_for("expected_StripMarkup"))
def test_strip_markup(value, expected):
    assert StripMarkup().clean(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"), cases_for("expected_WhitelistedStripMarkup")
)
def test_whitelisted_strip_markup(value, expected):
    assert WhitelistedStripMarkup().clean(value) == expected
