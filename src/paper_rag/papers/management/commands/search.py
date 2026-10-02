import json

from django.core.management.base import BaseCommand

from paper_rag.papers.search.search import SearchHit, hit_to_dict, search


class Command(BaseCommand):
    help = "Semantic search over the ingested papers."

    def add_arguments(self, parser):
        parser.add_argument("query")
        parser.add_argument("-k", type=int, default=5)
        parser.add_argument("--model")

    def handle(self, *args, **options):
        results: list[SearchHit] = search(options["query"], k=options["k"], model=options["model"])

        payload: dict[str, any] = {
            "query": options["query"],
            "results": [hit_to_dict(h) for h in results],
        }

        self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
