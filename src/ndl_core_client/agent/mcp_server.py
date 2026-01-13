"""MCP Server for NDL Core Client - Exposes search tools to AI agents."""

import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import search_agentic
from ..models import COLUMN_DESCRIPTIONS


# Initialize server
server = Server("ndl-core")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for AI agents."""
    return [
        Tool(
            name="search_ndl_corpus",
            description=(
                "Search the NDL Core Corpus for UK open government datasets. "
                "Returns datasets matching the semantic search query, including "
                "titles, descriptions, sources, licenses, and download URLs. "
                "Use this to find official UK government data on any topic."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query (e.g., 'police use of force statistics', 'NHS waiting times data')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10, max: 50)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_corpus_schema",
            description=(
                "Get the schema and field descriptions for the NDL Core Corpus. "
                "Use this to understand what fields are available in search results "
                "before or after searching."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls from AI agents."""

    if name == "search_ndl_corpus":
        query = arguments["query"]
        limit = min(arguments.get("limit", 10), 50)  # Cap at 50 results

        response = search_agentic(query, limit=limit)

        # Format results for agent consumption
        output = {
            "total_results": response.metadata.total_count,
            "returned_results": len(response.data),
            "results": [
                {
                    "title": r.get("title", ""),
                    "description": r.get("description", ""),
                    "source": r.get("source", ""),
                    "license": r.get("license", ""),
                    "format": r.get("format", ""),
                    "date": r.get("date", ""),
                    "tags": r.get("tags", []),
                    "download_urls": r.get("download", []),
                    "similarity_score": round(1 - r.get("_distance", 0), 4),
                }
                for r in response.data
            ]
        }

        return [TextContent(type="text", text=json.dumps(output, indent=2))]

    elif name == "get_corpus_schema":
        return [TextContent(type="text", text=json.dumps(COLUMN_DESCRIPTIONS, indent=2))]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def run_server():
    """Run the MCP server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Entry point for the MCP server."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
