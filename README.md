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

### Custom API URL

If you need to use a different API endpoint:

```python
from ndl_core_client import NDLCoreClient

# Create a client with a custom base URL
client = NDLCoreClient(base_url="https://your-custom-api-url.com")

# Search for datasets
results = client.search("your query")
```

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

## License

See [LICENSE](LICENSE) file for details.

