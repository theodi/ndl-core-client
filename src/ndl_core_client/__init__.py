"""NDL Core Client - A Python library to search the NDL Core Corpus."""

from .client import NDLCoreClient
from .models import AgentSearchResponse, SearchResultMetadata

__all__ = ["NDLCoreClient", "AgentSearchResponse", "SearchResultMetadata"]
