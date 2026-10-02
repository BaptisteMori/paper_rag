# Sources
from paper_rag.ingester.sources.inspire import InspireSource
from paper_rag.ingester.sources.source import Source

INGESTER_SOURCES: dict[str, Source] = {"inspire": InspireSource}
