# Sources
from paper_rag.ingester.sources.inspire import InspireSource
from paper_rag.ingester.sources.source import Source, SourceQuery  # noqa: F401

INGESTER_SOURCES: dict[str, Source] = {"inspire": InspireSource}
