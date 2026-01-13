"""NDL Core Client implementation."""

import requests
import pandas as pd

from .models import AgentSearchResponse, SearchResultMetadata


class NDLCoreClient:
    """Client for searching the NDL Core Corpus API."""

    def __init__(self, base_url: str = "https://theodi-ndl-core-data-api.hf.space") -> None:
        """Initialize the NDL Core Client.
        
        Args:
            base_url: The base URL of the NDL Core API (default: https://theodi-ndl-core-data-api.hf.space)
        """
        self.base_url = base_url.rstrip("/")

    def search(self, query: str) -> pd.DataFrame:
        """Search the NDL Core Corpus.
        
        Args:
            query: The search query string
            
        Returns:
            A pandas DataFrame containing the search results
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the API response format is unexpected
        """
        url = f"{self.base_url}/search"
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
        
        # Convert the list of JSON objects to a DataFrame
        df = pd.DataFrame(data)
        
        return df

    def search_agentic(self, query: str) -> AgentSearchResponse:
        """Search the NDL Core Corpus and return a Pydantic response for agentic use.
        
        This method is designed for use with AI agents and LLMs, returning a structured
        Pydantic object that includes both metadata and search results.
        
        Args:
            query: The search query string
            
        Returns:
            An AgentSearchResponse containing:
                - metadata: SearchResultMetadata with total_count and column_descriptions
                - data: List of search result dictionaries
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the API response format is unexpected
        """
        url = f"{self.base_url}/search"
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
        
        # Build metadata (column_descriptions uses default value)
        metadata = SearchResultMetadata(total_count=len(data))
        
        return AgentSearchResponse(
            metadata=metadata,
            data=data
        )
