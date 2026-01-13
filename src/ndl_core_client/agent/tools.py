"""Agent tools for searching the NDL Core Corpus."""

from typing import Optional

import requests

from ..models import AgentSearchResponse, SearchResultMetadata


DEFAULT_BASE_URL = "https://theodi-ndl-core-data-api.hf.space"


def search_agentic(
    query: str,
    base_url: str = DEFAULT_BASE_URL,
    limit: Optional[int] = None,
) -> AgentSearchResponse:
    """Search the NDL Core Corpus and return a structured response for agentic use.

    This function is designed for use with AI agents and LLMs, returning a structured
    Pydantic object that includes both metadata and search results.

    Args:
        query: The natural language search query string
            (e.g., "police use of force statistics", "NHS waiting times data")
        base_url: The base URL of the NDL Core API
            (default: https://theodi-ndl-core-data-api.hf.space)
        limit: Maximum number of results to return. If None, returns all results.

    Returns:
        An AgentSearchResponse containing:
            - metadata: SearchResultMetadata with total_count and column_descriptions
            - data: List of search result dictionaries

    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If the API response format is unexpected

    Example:
        >>> from ndl_core_client.agent import search_agentic
        >>> response = search_agentic("renewable energy data", limit=5)
        >>> print(f"Found {response.metadata.total_count} results")
        >>> for result in response.data:
        ...     print(result['title'])
    """
    url = f"{base_url.rstrip('/')}/search"
    params = {"query": query}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    # Validate that the response is a list
    if not isinstance(data, list):
        raise ValueError(
            f"Expected API to return a list, got {type(data).__name__}. "
            f"Response: {data}"
        )

    # Apply limit if specified
    if limit is not None:
        data = data[:limit]

    # Build metadata (column_descriptions uses default value)
    metadata = SearchResultMetadata(total_count=len(data))

    return AgentSearchResponse(
        metadata=metadata,
        data=data
    )
