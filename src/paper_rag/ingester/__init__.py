from paper_rag.ingester.sources.ingester import Source, SourceQuery

# Sources
from paper_rag.ingester.sources.inspire import InspireSource

INGESTER_SOURCES: dict[str:Source] = {"inspire": InspireSource}
