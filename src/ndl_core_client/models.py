"""Pydantic models for NDL Core Client."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


COLUMN_DESCRIPTIONS: Dict[str, str] = {
    "identifier": "string (UUID). Globally unique identifier for the record.",
    "title": "string. Title of the resource or filename where a title is not available.",
    "description": "string. Human-readable description or summary of the resource.",
    "source": "string. Origin of the data (e.g. gov.uk, ons.gov.uk, legislation.gov.uk).",
    "date": "date (ISO 8601). Original publication or creation date of the resource, where available.",
    "collection_time": "datetime (ISO 8601). Timestamp indicating when the data was crawled or ingested into the corpus.",
    "open_type": "string. Classification of the openness context (e.g. Open Government, Open Data, Open Source).",
    "license": "string. Usage and redistribution rights associated with the resource.",
    "tags": "array[string]. Automatically assigned EU Data Theme Vocabulary tags describing the content domain.",
    "language": "string (ISO 639-1). Automatically detected language of the resource content.",
    "format": "string. Data format of the record (e.g. text, parquet).",
    "text": "string. Preview of the extracted textual content of the resource (first 100 characters only).",
    "word_count": "integer. Number of space-delimited words in the text field.",
    "token_count": "integer. Number of tokens calculated using the embedding model tokenizer.",
    "data_file": "string. Relative path to the associated structured data file, if applicable. Data files exist in the ndl-core-structured-data dataset.",
    "extra_metadata": "object. Source-specific, sparse metadata not covered by the core schema.",
    "_distance": "double. Similarity score from the semantic search (cosine distance). Lower values indicate higher similarity.",
    "download": "array[string]. One or more URLs where the dataset can be downloaded."
}


class SearchResultMetadata(BaseModel):
    """Metadata about the search results."""
    
    total_count: int = Field(
        description="Total number of search results returned."
    )
    column_descriptions: Dict[str, str] = Field(
        default=COLUMN_DESCRIPTIONS,
        description="Schema describing each column/field in the search results."
    )


class AgentSearchResponse(BaseModel):
    """Response model for agentic search containing metadata and search results."""
    
    metadata: SearchResultMetadata = Field(
        description="Metadata about the search results including field descriptions."
    )
    data: List[Dict[str, Any]] = Field(
        description="List of search results matching the query."
    )
