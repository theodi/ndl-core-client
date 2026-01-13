# NDL Core Client

[![Try In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/theodi/ndl-core-client/blob/main/demo.ipynb)

> **Note:** The backend API is hosted on [Hugging Face Spaces](https://huggingface.co/spaces/theodi/ndl-core-data-api) using the free tier. If you experience connection timeouts, please visit the Space URL first to wake up the service, then retry your request.

A Python library to easily search and download datasets from the NDL Core Corpus.

## Installation

You can install the library directly from GitHub using pip:

```bash
pip install git+https://github.com/theodi/ndl-core-client.git
```

## Usage

The library provides a simple `NDLCoreClient` class with a `search` function to query the NDL Core Corpus API.

See the notebook for usage details: [![Try In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/theodi/ndl-core-client/blob/main/demo.ipynb)

### Basic Example

```python
from ndl_core_client import NDLCoreClient

# Create a client instance
client = NDLCoreClient()

# Search for datasets
results = client.search("Police use of force")

# Results are returned as a pandas DataFrame
print(results)
```

### Agentic Search (for AI Agents & LLMs)

For use with AI agents and LLMs, use `search_agentic` which returns a structured Pydantic object:

```python
from ndl_core_client import NDLCoreClient

# Create a client instance
client = NDLCoreClient()

# Search and get structured response
response = client.search_agentic("Police use of force")

# Access metadata (total count and column descriptions)
print(f"Total results: {response.metadata.total_count}")
print(f"Column descriptions: {response.metadata.column_descriptions}")

# Access search results as list of dictionaries
for result in response.data:
    print(f"Title: {result['title']}")
    print(f"Source: {result['source']}")
    print(f"Distance: {result['_distance']}")
```

### Custom API URL

If you need to use a different API endpoint:

```python
from ndl_core_client import NDLCoreClient

# Create a client with a custom base URL
client = NDLCoreClient(base_url="https://your-custom-api-url.com")

# Search for datasets
results = client.search("your query")

## Development

This project uses [uv](https://github.com/astral-sh/uv) as the package manager.

### Setup

1. Install uv:
```bash
pip install uv
```

2. Install dependencies:
```bash
uv sync
```

## API Reference

### NDLCoreClient

The main client class for interacting with the NDL Core Corpus API.

#### `__init__(base_url: str = "https://theodi-ndl-core-data-api.hf.space")`

Initialize the client.

**Parameters:**
- `base_url` (str, optional): The base URL of the NDL Core API. Defaults to "https://theodi-ndl-core-data-api.hf.space".

#### `search(query: str) -> pd.DataFrame`

Search the NDL Core Corpus.

**Parameters:**
- `query` (str): The search query string.

**Returns:**
- `pd.DataFrame`: A pandas DataFrame containing the search results.

**Raises:**
- `requests.exceptions.RequestException`: If the API request fails.

#### `search_agentic(query: str) -> AgentSearchResponse`

Search the NDL Core Corpus and return a Pydantic response for agentic use.

**Parameters:**
- `query` (str): The search query string.

**Returns:**
- `AgentSearchResponse`: A Pydantic object containing:
  - `metadata` (SearchResultMetadata): Contains `total_count` and `column_descriptions`
  - `data` (List[Dict[str, Any]]): List of search results as dictionaries

**Raises:**
- `requests.exceptions.RequestException`: If the API request fails.

### SearchResultMetadata

Pydantic model containing metadata about the search results:

- `total_count` (int): Total number of search results returned
- `column_descriptions` (Dict[str, str]): Schema describing each column/field in the search results

### AgentSearchResponse

Pydantic model for the agentic search response:

- `metadata` (SearchResultMetadata): Metadata about the search results
- `data` (List[Dict[str, Any]]): List of search results matching the query

### Column Descriptions

The following fields are available in each search result:

| Field | Type | Description |
|-------|------|-------------|
| `identifier` | str (UUID) | Globally unique identifier for the record |
| `title` | str | Title of the resource or filename where a title is not available |
| `description` | str | Human-readable description or summary of the resource |
| `source` | str | Origin of the data (e.g. gov.uk, ons.gov.uk, legislation.gov.uk) |
| `date` | date (ISO 8601) | Original publication or creation date of the resource |
| `collection_time` | datetime (ISO 8601) | Timestamp when the data was crawled or ingested |
| `open_type` | str | Classification of openness context (e.g. Open Government, Open Data) |
| `license` | str | Usage and redistribution rights associated with the resource |
| `tags` | List[str] | EU Data Theme Vocabulary tags describing the content domain |
| `language` | str (ISO 639-1) | Automatically detected language of the resource content |
| `format` | str | Data format of the record (e.g. text, parquet) |
| `text` | str | Preview of extracted textual content (first 100 characters) |
| `word_count` | int | Number of space-delimited words in the text field |
| `token_count` | int | Number of tokens calculated using the embedding model tokenizer |
| `data_file` | str | Relative path to structured data file in ndl-core-structured-data dataset |
| `extra_metadata` | Dict[str, Any] | Source-specific metadata not covered by the core schema |
| `_distance` | float | Search similarity score (cosine distance). Lower is more similar |
| `download` | List[str] | Data download URLs |

## License

See [LICENSE](LICENSE) file for details.

