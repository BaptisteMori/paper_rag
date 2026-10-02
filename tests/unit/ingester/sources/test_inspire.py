from dataclasses import dataclass

import httpx
import pytest

from paper_rag.ingester.sources.inspire import InspireSource
from paper_rag.ingester.sources.source import SourceQuery


def make_hit(recid: int, with_abstract: bool = True) -> dict:
    """Fabrique une notice au format de l'API INSPIRE (seulement les champs utilisés)."""
    metadata = {
        "control_number": recid,
        "titles": [{"title": f"Title {recid}"}],
        "authors": [{"full_name": "Doe, J."}],
        "earliest_date": "2024-05-01",
    }
    if with_abstract:
        metadata["abstracts"] = [{"value": f"Abstract {recid}"}]
    return {"id": str(recid), "metadata": metadata}


@dataclass
class ProducedResponse:
    url: str
    page: dict[str, any]
    status_code: int = 200


def make_handler(responses: dict[str, ProducedResponse]):

    def handler(request: httpx.Request):
        response: ProducedResponse = responses.get(request.url.params.get("page", "1"))
        return httpx.Response(response.status_code, json=response.page)

    return handler


def make_source(handler) -> InspireSource:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return InspireSource(delay=0, client=client)


def test_parse_valid_hit():
    source = make_source(lambda request: httpx.Response(200))
    record = source.parse(make_hit(42))

    assert record.source == "inspire"
    assert record.external_id == "42"
    assert record.title == "Title 42"
    assert record.authors == ["Doe, J."]
    assert record.url.endswith("/42")


def test_parse_skips_hit_without_abstract():
    source = make_source(lambda request: httpx.Response(200))
    assert source.parse(make_hit(1, with_abstract=False)) is None


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (SourceQuery(text="dark matter"), '"dark matter"'),
        (SourceQuery(title="higgs"), "t higgs"),
        (SourceQuery(authors=["Doe, J."]), 'a "Doe, J."'),
        (SourceQuery(title="higgs", keywords=["lhc"]), "t higgs and k lhc"),
    ],
)
def test_parse_query(query, expected):
    source = make_source(lambda request: httpx.Response(200))
    assert source._parse_query(query) == expected


def test_parse_query_empty_query_is_rejected():
    source = make_source(lambda request: httpx.Response(200))
    with pytest.raises(ValueError):
        source._parse_query(SourceQuery())


def test_fetch_follows_next_link_and_stops_at_limit():
    response2: ProducedResponse = ProducedResponse(
        url="https://inspirehep.net/api/literature?page=2",
        page={
            "hits": {"hits": [make_hit(3), make_hit(4)]},
            "links": {},
        },
    )

    response1: ProducedResponse = ProducedResponse(
        url="https://inspirehep.net/api/literature?q=t+x&size=3&fields=control_number%2Ctitles%2Cabstracts%2Cauthors.full_name%2Cearliest_date&sort=mostrecent",
        page={
            "hits": {"hits": [make_hit(1), make_hit(2)]},
            "links": {"next": response2.url},
        },
    )

    responses: dict[str, ProducedResponse] = {
        "1": response1,
        "2": response2,
    }

    source: InspireSource = make_source(make_handler(responses))

    records = list(source.fetch(SourceQuery(title="x"), limit=3))
    assert [r.external_id for r in records] == ["1", "2", "3"]
