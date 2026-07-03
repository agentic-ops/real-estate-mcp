"""Real Estate MCP Server -- main entry point.

A comprehensive Model Context Protocol server for real estate data
management. Initializes a FastMCP server, registers all enabled tools,
resources, and prompts, and runs the selected transport. A module-level
``mcp`` instance is exposed so the MCP Inspector / CLI can load it directly::

    mcp dev main.py:mcp

Transport, host, and port are configurable via CLI flags or the
``MCP_TRANSPORT`` / ``HOST`` / ``PORT`` environment variables. The default
transport is ``stdio`` (for Claude Desktop compatibility); pass ``sse`` (or
``--transport sse``) for remote/web access. The legacy ``python main.py sse``
invocation is still supported.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Literal, cast

from mcp.server.fastmcp import FastMCP

from feature_flags import enabled_categories
from prompts import register_all_prompts
from resources import register_all_resources
from tools import register_all_tools
from utils import audit, get_data_manager

SERVER_NAME = "Real Estate MCP Server"
SERVER_VERSION = "2.0.0"
INSTRUCTIONS = (
    "Comprehensive real estate workflow tools for property search and "
    "insights, agent and client management, market and area intelligence, "
    "mortgage/affordability math, comparable-based valuation, and investment "
    "analysis. Operates on local seed data with optional opt-in live "
    "integrations. Provides workflow augmentation, not financial or legal advice."
)
TRANSPORTS = ["stdio", "sse", "streamable-http"]

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("real_estate_mcp")


def create_server(host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    """Build and fully configure the FastMCP server instance."""

    server = FastMCP(
        SERVER_NAME,
        instructions=INSTRUCTIONS,
        host=host,
        port=port,
    )
    register_all_tools(server)
    register_all_resources(server)
    register_all_prompts(server)

    stats = get_data_manager().stats()
    categories = enabled_categories()
    logger.info("%s v%s starting", SERVER_NAME, SERVER_VERSION)
    logger.info("Loaded real estate data: %s", stats)
    logger.info("Enabled tool categories: %s", categories)
    audit(
        "server_initialized",
        version=SERVER_VERSION,
        enabled_categories=categories,
        **stats,
    )
    return server


# Module-level instance for `mcp dev main.py:mcp` and imports.
mcp = create_server(
    host=os.environ.get("HOST", "127.0.0.1"),
    port=int(os.environ.get("PORT", "8000")),
)


def _resolve_transport(args: argparse.Namespace) -> str:
    """Resolve the transport from --transport, a positional arg, or env."""

    return (
        args.transport
        or args.transport_positional
        or os.environ.get("MCP_TRANSPORT")
        or "stdio"
    )


def main() -> None:
    """Parse arguments and run the Real Estate MCP Server."""

    parser = argparse.ArgumentParser(description=f"{SERVER_NAME} v{SERVER_VERSION}")
    parser.add_argument(
        "transport_positional",
        nargs="?",
        choices=TRANSPORTS,
        default=None,
        help="Transport protocol (legacy positional form, e.g. 'sse').",
    )
    parser.add_argument(
        "--transport",
        choices=TRANSPORTS,
        default=None,
        help="Transport protocol (overrides positional and MCP_TRANSPORT).",
    )
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()

    transport = _resolve_transport(args)
    mcp.settings.host = args.host
    mcp.settings.port = args.port

    logger.info(
        "Running %s (transport=%s, host=%s, port=%s)",
        SERVER_NAME,
        transport,
        args.host,
        args.port,
    )
    mcp.run(transport=cast(Literal["stdio", "sse", "streamable-http"], transport))


if __name__ == "__main__":
    main()
