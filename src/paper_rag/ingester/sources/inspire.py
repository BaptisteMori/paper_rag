import time
from collections.abc import Iterator

import httpx

from paper_rag.core.business_object.paper_record import PaperRecord
from paper_rag.core.utils import config, dates
from paper_rag.ingester.sources.ingester import Source, SourceQuery


class InspireSource(Source):
    """INSPIRE-HEP literature API: https://github.com/inspirehep/rest-api-doc"""

    name = "inspire"

    def __init__(
        self,
        default_page_size: int = 50,
        delay: float = 1.0,
        client: httpx.Client | None = None,
    ):
        self.default_page_size: int = default_page_size
        self.delay: float = delay  # INSPIRE rate-limits: stay polite
        self.client: httpx.Client = client or httpx.Client(timeout=30)
        self.url: str = config()["sources"][self.name]["url"]
        self.api_url: str = config()["sources"][self.name]["api_url"]
        self.fields: list[str] = config()["sources"][self.name]["fields"]

    @staticmethod
    def _quote(value: str) -> str:
        cleaned = value.replace('"', "").strip()
        return f'"{cleaned}"' if " " in cleaned else cleaned

    def _get(self, url: str, params: dict | None, retries: int = 3) -> httpx.Response:
        for _ in range(retries):
            resp = self.client.get(url, params=params)
            if resp.status_code != 429:
                resp.raise_for_status()
                return resp
            time.sleep(5)  # la doc impose d'attendre au moins 5 s après un 429
        resp.raise_for_status()
        return resp

    def _parse_query(self, query: SourceQuery) -> str:
        """Translate a query to a qurey for INSPIRE."""
        clauses: list[str] = []

        if query.text:
            clauses.append(self._quote(query.text))
        if query.title:
            clauses.append(f"t {self._quote(query.title)}")
        for author in query.authors:
            clauses.append(f"a {self._quote(author)}")
        for keyword in query.keywords:
            clauses.append(f"k {self._quote(keyword)}")
        if query.since:
            clauses.append(f"date >= {query.since.isoformat()}")
        if query.until:
            clauses.append(f"date <= {query.until.isoformat()}")
        if query.raw:
            clauses.append(f"({query.raw})")

        if not clauses:
            raise ValueError("SourceQuery is empty: at least one criterion is required")
        return " and ".join(clauses)

    def fetch(
        self, query: SourceQuery, limit: int = 100, sort: str = "mostrecent"
    ) -> Iterator[PaperRecord]:
        limit: int = min(limit, config()["sources"][self.name]["max_results"])
        nb_records: int = 0
        url: str | None = self.api_url
        params: dict = {
            "q": self._parse_query(query),
            "size": min(self.default_page_size, limit),
            "fields": ",".join(self.fields),
            "sort": sort,  # "mostrecent" ou "mostcited"
        }

        while url and nb_records < limit:
            resp: httpx.Response = self._get(url, params)
            data: dict = resp.json()

            for hit in data.get("hits", {}).get("hits", []):
                if (record := self.parse(hit)) is None:
                    continue
                yield record
                nb_records += 1
                if nb_records >= limit:
                    return

            url = data.get("links", {}).get("next")  # None à la dernière page
            params = None  # l'URL "next" contient déjà tous les paramètres
            time.sleep(self.delay)

    def parse(self, hit: dict) -> PaperRecord | None:

        md = hit.get("metadata", {})
        abstracts = md.get("abstracts") or []

        if not abstracts:
            return None  # nothing useful to embed

        recid = str(md.get("control_number", hit.get("id")))
        return PaperRecord(
            source=self.name,
            external_id=recid,
            title=(md.get("titles") or [{}])[0].get("title", ""),
            abstract=abstracts[0].get("value", ""),
            authors=[a.get("full_name", "") for a in (md.get("authors") or [])][:20],
            published=dates.parse_date(md.get("earliest_date")),
            url=f"{self.url}{recid}",
        )
