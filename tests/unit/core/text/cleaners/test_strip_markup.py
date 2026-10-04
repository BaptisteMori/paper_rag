import pytest

from paper_rag.core.text.cleaners.strip_markup import (
    StripMarkup,
    WhitelistedStripMarkup,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            (
                "of the di-J/ψ spectrum. The CMS angular analysis favors "
                '<math altimg="si19.svg"><mrow><msup><mi>J</mi>'
                "<mrow><mi>P</mi><mi>C</mi></mrow></msup>"
                '<mo linebreak="goodbreak">=</mo><msup><mn>2</mn>'
                "<mrow><mo>+</mo><mo>+</mo></mrow></msup></mrow></math>, "
                "motivating a spin-two mediator rather than the scalar ansatz "
                "used in earlier versions of this study."
            ),
            (
                "of the di-J/ψ spectrum. The CMS angular analysis favors "
                "JPC=2++, motivating a spin-two mediator rather than the scalar "
                "ansatz used in earlier versions of this study."
            ),
        ),
        (
            '<mi mathvariant="script">x</mi>',
            "x",
        ),
        (
            "a < b and c > d",
            "a < b and c > d",
        ),
        (
            "E<5 GeV and p>2",
            "E<5 GeV and p>2",
        ),
        (
            "x<y and z>w",
            "xw",  # <= here, strip to general
        ),
        (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of> inelasti",
            "on zero. A dedicated LZ search over $271 inelasti",  # <= here, strip to general
        ),
        (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti",
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti",
        ),
    ],
)
def test_strip_markup(value, expected):
    assert StripMarkup().clean(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            (
                "of the di-J/ψ spectrum. The CMS angular analysis favors "
                '<math altimg="si19.svg"><mrow><msup><mi>J</mi>'
                "<mrow><mi>P</mi><mi>C</mi></mrow></msup>"
                '<mo linebreak="goodbreak">=</mo><msup><mn>2</mn>'
                "<mrow><mo>+</mo><mo>+</mo></mrow></msup></mrow></math>, "
                "motivating a spin-two mediator rather than the scalar ansatz "
                "used in earlier versions of this study."
            ),
            (
                "of the di-J/ψ spectrum. The CMS angular analysis favors "
                "JPC=2++, motivating a spin-two mediator rather than the scalar "
                "ansatz used in earlier versions of this study."
            ),
        ),
        (
            '<mi mathvariant="script">x</mi>',
            "x",
        ),
        (
            "a < b and c > d",
            "a < b and c > d",
        ),
        (
            "E<5 GeV and p>2",
            "E<5 GeV and p>2",
        ),
        (
            "x<y and z>w",
            "x<y and z>w",
        ),
        (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of> inelasti",
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of> inelasti",
        ),
        (
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti",
            "on zero. A dedicated LZ search over "
            "$271<E_R<800\\,{\\rm keV}$ would provide a decisive test of inelasti",
        ),
    ],
)
def test_whitelisted_strip_markup(value, expected):
    assert WhitelistedStripMarkup().clean(value) == expected
