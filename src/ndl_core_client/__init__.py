"""NDL Core Client - A Python library to search the NDL Core Corpus."""

from .client import NDLCoreClient
from .models import AgentSearchResponse, SearchResultMetadata, COLUMN_DESCRIPTIONS
from .agent.tools import search_agentic

__all__ = [
    "NDLCoreClient",
    "AgentSearchResponse",
    "SearchResultMetadata",
    "COLUMN_DESCRIPTIONS",
    "search_agentic",
]
