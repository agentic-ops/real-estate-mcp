"""
Real Estate MCP Server

A comprehensive Model Context Protocol server for real estate data management.
Provides tools, resources, and prompts for property listings, agent management,
market analysis, client relationships, and area intelligence.
"""

import asyncio

from mcp.server.fastmcp import FastMCP

from prompts import register_all_prompts
from resources.resource_templates import register_resource_templates
from resources.static_resources import register_static_resources
from tools.agent_tools import register_agent_tools
from tools.area_tools import register_area_tools
from tools.client_tools import register_client_tools
from tools.market_tools import register_market_tools

# Import all component registration functions
from tools.property_tools import register_property_tools
from tools.system_tools import register_system_tools
from utils import data_manager

# Create the FastMCP server
mcp = FastMCP("Real Estate MCP Server")


def register_all_components():
    """Register all tools, resources, and prompts with the MCP server"""

    # Register all tool categories
    register_property_tools(mcp)
    register_agent_tools(mcp)
    register_market_tools(mcp)
    register_client_tools(mcp)
    register_area_tools(mcp)
    register_system_tools(mcp)

    # Register all resources
    register_static_resources(mcp)
    register_resource_templates(mcp)

    # Register all prompts
    register_all_prompts(mcp)


async def main():
    """Main server function"""
    # Register all components
    register_all_components()

    # Print startup information
    print("🏠 Real Estate MCP Server Starting...")
    print(f"📊 Loaded {len(data_manager.get_all_properties())} properties")
    print(f"👥 Loaded {len(data_manager.get_all_agents())} agents")
    print(f"🏢 Loaded {len(data_manager.get_all_clients())} clients")
    print(f"📈 Loaded {len(data_manager.get_recent_sales())} recent sales")
    print(f"🌍 Loaded {len(data_manager.get_all_areas())} areas")
    print("✅ Server ready for connections!")

    # Run the server with SSE transport using FastMCP's built-in functionality
    print("🌐 SSE Server running on http://127.0.0.1:8000/sse")
    print("📡 Ready for MCP client connections")

    await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())
