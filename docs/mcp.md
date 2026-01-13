# Using NDL Core Client with AI Agents (MCP)

This library provides a **Model Context Protocol (MCP)** server for seamless integration with AI agents like Claude, Gemini, OpenAI, and others.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that enables AI agents to securely connect to external tools and data sources. By providing an MCP server, NDL Core Client can be used directly by AI assistants to search UK government datasets.

## Project Structure

The agent-related functionality is organized in the `ndl_core_client.agent` module:

```
ndl_core_client/
├── agent/
│   ├── __init__.py      # Agent module exports
│   ├── tools.py         # search_agentic function
│   └── mcp_server.py    # MCP server implementation
├── client.py            # NDLCoreClient class
└── models.py            # Pydantic models
```

## Direct Usage (Without MCP)

For programmatic use in your own agents or applications, use the `search_agentic` function directly:

```python
from ndl_core_client import search_agentic

# Search with a natural language query
response = search_agentic("NHS waiting times data", limit=10)

# Access structured results
print(f"Found {response.metadata.total_count} results")
for result in response.data:
    print(f"- {result['title']} ({result['source']})")
    print(f"  Download: {result['download']}")
```

## Installation

Install the library with MCP support:

```bash
pip install "ndl-core-client[mcp] @ git+https://github.com/theodi/ndl-core-client.git"
```

Or with uv:

```bash
uv pip install "ndl-core-client[mcp] @ git+https://github.com/theodi/ndl-core-client.git"
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `search_ndl_corpus` | Search for UK government datasets by natural language query |
| `get_corpus_schema` | Get field descriptions for understanding search results |

### Tool: `search_ndl_corpus`

Search the NDL Core Corpus for UK open government datasets.

**Parameters:**
- `query` (string, required): Natural language search query (e.g., "police use of force statistics", "NHS waiting times data")
- `limit` (integer, optional): Maximum number of results to return (default: 10, max: 50)

**Returns:** JSON object containing:
- `total_results`: Total number of matching datasets
- `returned_results`: Number of results returned
- `results`: Array of dataset objects with title, description, source, license, format, date, tags, download_urls, and similarity_score

### Tool: `get_corpus_schema`

Get the schema and field descriptions for the NDL Core Corpus.

**Parameters:** None

**Returns:** JSON object mapping field names to their descriptions

---

## Claude Desktop

Add to your Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ndl-core": {
      "command": "ndl-core-mcp"
    }
  }
}
```

Restart Claude Desktop, then you can ask:

> "Find me UK government datasets about NHS waiting times"

Claude will automatically use the `search_ndl_corpus` tool to find relevant datasets.

---

## Gemini (Google AI Studio / Vertex AI)

Gemini supports MCP tools through the Google AI SDK. First, ensure the MCP server is installed, then configure your Gemini agent:

```python
from google import genai
from google.genai import types

# Create MCP tools from the server
tools = types.Tool(mcp=types.MCPTool(
    command="ndl-core-mcp"
))

# Initialize Gemini client
client = genai.Client()

# Create a chat with MCP tools enabled
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(tools=[tools])
)

# Gemini can now use the NDL Core search tools
response = chat.send_message("Find UK government data about renewable energy")
print(response.text)
```

For Vertex AI, use the `vertexai` package with similar configuration.

---

## OpenAI Agents

OpenAI's Agents SDK supports MCP tools for building AI agents that can use external tools.

### Using with OpenAI Agents SDK

```python
import asyncio
from openai import agents
from agents.mcp import MCPServerStdio

async def main():
    # Create MCP server connection
    async with MCPServerStdio(
        command="ndl-core-mcp"
    ) as mcp_server:
        # Get tools from the MCP server
        tools = await mcp_server.list_tools()
        
        # Create an agent with MCP tools
        agent = agents.Agent(
            name="UK Data Research Agent",
            instructions="You help users find UK government datasets. Use the search_ndl_corpus tool to find relevant data.",
            tools=tools
        )
        
        # Run the agent
        result = await agents.Runner.run(
            agent,
            "Find datasets about air quality monitoring in London"
        )
        
        print(result.final_output)

asyncio.run(main())
```

### Using with OpenAI Responses API (Direct Tool Calling)

If you prefer direct API access without the Agents SDK, you can use the MCP tools with the Responses API:

```python
import subprocess
import json
from openai import OpenAI

client = OpenAI()

# Define the tools based on MCP schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_ndl_corpus",
            "description": "Search the NDL Core Corpus for UK open government datasets. Returns datasets matching the semantic search query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Use with chat completions
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Find UK datasets about climate change policies"}],
    tools=tools
)

# Handle tool calls by invoking the MCP server
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    # Process tool call with MCP server...
```

### Using with OpenAI Assistants API

For persistent agents with memory, configure MCP tools in your Assistant:

```python
from openai import OpenAI

client = OpenAI()

# Create an assistant with NDL Core tools
assistant = client.beta.assistants.create(
    name="UK Government Data Researcher",
    instructions="You help users find and analyze UK government open data. Use the available tools to search the NDL Core Corpus.",
    model="gpt-4o",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "search_ndl_corpus",
                "description": "Search the NDL Core Corpus for UK open government datasets.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Natural language search query"},
                        "limit": {"type": "integer", "description": "Max results (default: 10)"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "get_corpus_schema",
                "description": "Get field descriptions for NDL Core Corpus search results.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        }
    ]
)

print(f"Created assistant: {assistant.id}")
```

---

## Other MCP-Compatible Clients

The NDL Core MCP server works with any MCP-compatible client. The server uses **stdio transport**, meaning it communicates via standard input/output.

### Generic Usage

```bash
# Run the MCP server directly
ndl-core-mcp
```

The server accepts JSON-RPC messages on stdin and responds on stdout, following the MCP specification.

### Environment Variables

No environment variables are required. The server connects to the default NDL Core API endpoint.

---

## Example Interactions

Once configured, you can ask your AI agent natural language questions like:

- "Find UK government datasets about NHS waiting times"
- "Search for open data on police use of force statistics"  
- "What datasets are available about renewable energy in the UK?"
- "Find data about housing prices from the Office for National Statistics"
- "Search for environmental monitoring data from DEFRA"

The agent will use the `search_ndl_corpus` tool to find relevant datasets and present the results, including titles, descriptions, sources, and download links.
