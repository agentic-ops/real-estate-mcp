"""
Market resources for the Real Estate MCP Server
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import data_manager


def register_market_resources(mcp: FastMCP):
    """Register all market-related resources with the MCP server"""

    @mcp.resource("realestate://market-overview")
    def get_market_overview_resource() -> str:
        """Current market overview and trends"""
        overview = data_manager.get_market_overview()
        return json.dumps(overview, indent=2)

    @mcp.resource("realestate://market/area/{area}")
    def get_area_market_resource(area: str) -> str:
        """Market analysis for a specific area"""
        market_data = data_manager.get_area_market_data(area)
        area_info = data_manager.get_area_info(area)
        sales = data_manager.get_sales_by_area(area)

        return json.dumps(
            {
                "area": area,
                "area_info": area_info,
                "market_data": market_data,
                "recent_sales_count": len(sales),
                "recent_sales": sales,
            },
            indent=2,
        )
