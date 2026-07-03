"""
System and data management MCP tools
"""

import json

from mcp.server.fastmcp import FastMCP

from feature_flags import enabled_categories
from utils import audit, data_manager


def register_system_tools(mcp: FastMCP):
    """Register all system and data management tools with the MCP server"""

    @mcp.tool()
    def refresh_data() -> str:
        """Refresh all cached data from files"""
        audit("refresh_data")
        data_manager.refresh_data()
        return "Data cache refreshed successfully"

    @mcp.tool()
    def get_server_info() -> str:
        """Get server version, data statistics, and enabled tool categories."""
        audit("get_server_info")
        return json.dumps(
            {
                "server": "Real Estate MCP Server",
                "version": "2.0.0",
                "data_stats": data_manager.stats(),
                "enabled_categories": enabled_categories(),
            },
            indent=2,
        )

    @mcp.tool()
    def get_data_summary() -> str:
        """Get summary statistics of all data in the system"""
        summary = {
            "properties": {
                "total_active_listings": len(data_manager.get_all_properties()),
                "price_range": data_manager.properties.get("price_range", {}),
            },
            "agents": {"total_agents": len(data_manager.get_all_agents())},
            "clients": {
                "total_clients": len(data_manager.get_all_clients()),
                "lead_sources": data_manager.clients.get("lead_sources", {}),
            },
            "sales": {
                "total_recent_sales": len(data_manager.get_recent_sales()),
                "sales_summary": data_manager.transactions.get("sales_summary", {}),
            },
            "areas": {
                "total_areas": len(data_manager.get_all_areas()),
                "city_info": {
                    "name": data_manager.areas.get("city_name"),
                    "population": data_manager.areas.get("population"),
                },
            },
            "market": {
                "current_market_type": data_manager.market.get(
                    "market_overview", {}
                ).get("market_type"),
                "avg_days_on_market": data_manager.market.get(
                    "market_overview", {}
                ).get("avg_days_on_market"),
            },
        }

        return json.dumps(summary, indent=2)
