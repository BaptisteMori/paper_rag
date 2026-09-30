from dataclasses import fields
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from paper_rag.core.embedders import get_embedder
from paper_rag.ingester import INGESTER_SOURCES
from paper_rag.ingester.ingester import ingest
from paper_rag.ingester.sources.ingester import SourceQuery


class Command(BaseCommand):
    help = "Fetch papers from a source and store them in PostgreSQL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", default="inspire", choices=list(INGESTER_SOURCES)
        )
        parser.add_argument("--limit", type=int, default=200)
        parser.add_argument("--text")
        parser.add_argument("--title")
        parser.add_argument("--author", dest="authors", action="append", default=[])
        parser.add_argument("--keyword", dest="keywords", action="append", default=[])
        parser.add_argument("--since", type=date.fromisoformat)
        parser.add_argument("--until", type=date.fromisoformat)
        parser.add_argument("--raw")
        parser.add_argument("--embedder", dest="provider")
        parser.add_argument("--model")

    def handle(self, *args, **options):
        names = {f.name for f in fields(SourceQuery)}
        query = SourceQuery(**{k: v for k, v in options.items() if k in names})
        if not any([query.text, query.title, query.authors, query.keywords, query.raw]):
            raise CommandError(
                "Give at least one of --text, --title, --author, --keyword, --raw"
            )

        source = INGESTER_SOURCES[options["source"]]()

        embedder = get_embedder(options["provider"], options["model"])
        papers, embedded = ingest(source, query, options["limit"], embedder)
        self.stdout.write(
            self.style.SUCCESS(f"{papers} papers, {embedded} embeddings computed")
        )
