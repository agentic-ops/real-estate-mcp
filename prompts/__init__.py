"""
Central prompt registration for the Real Estate MCP Server

This module imports and registers all prompt categories with the MCP server.
Provides a single entry point for prompt initialization.
"""

from mcp.server.fastmcp import FastMCP

from .agent_prompts import register_agent_prompts
from .client_prompts import register_client_prompts
from .finance_prompts import register_finance_prompts
from .market_prompts import register_market_prompts
from .property_prompts import register_property_prompts


def register_all_prompts(mcp: FastMCP):
    """
    Register all prompt templates with the MCP server

    This function imports and registers prompts from all categories:
    - Property prompts: Property analysis and comparison
    - Client prompts: Client matching and consultation
    - Market prompts: Market analysis and investment opportunities
    - Agent prompts: Agent performance and business development

    Args:
        mcp: The FastMCP server instance to register prompts with
    """

    # Register all prompt categories
    register_property_prompts(mcp)
    register_client_prompts(mcp)
    register_market_prompts(mcp)
    register_agent_prompts(mcp)
    register_finance_prompts(mcp)


# Export the main registration function
__all__ = ["register_all_prompts"]
