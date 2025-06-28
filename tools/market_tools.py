"""
Market analysis MCP tools
"""

import json
from mcp.server.fastmcp import FastMCP
from utils import data_manager


def register_market_tools(mcp: FastMCP):
    """Register all market analysis tools with the MCP server"""
    
    @mcp.tool()
    def get_market_overview() -> str:
        """Get overall market overview and trends"""
        overview = data_manager.get_market_overview()
        return json.dumps(overview, indent=2)

    @mcp.tool()
    def get_price_analytics() -> str:
        """Get comprehensive price analytics and market data"""
        analytics = data_manager.get_price_analytics()
        return json.dumps(analytics, indent=2)

    @mcp.tool()
    def get_area_market_data(area: str) -> str:
        """Get market performance data for a specific area"""
        market_data = data_manager.get_area_market_data(area)
        if market_data:
            return json.dumps({
                "area": area,
                "market_data": market_data
            }, indent=2)
        return f"Market data for area '{area}' not found"

    @mcp.tool()
    def compare_areas(areas: str) -> str:
        """Compare market data across multiple areas (comma-separated list)"""
        area_list = [area.strip() for area in areas.split(",")]
        comparison = data_manager.compare_areas(area_list)
        
        return json.dumps({
            "areas_compared": area_list,
            "comparison": comparison
        }, indent=2)

    @mcp.tool()
    def get_investment_opportunities() -> str:
        """Get investment opportunities and rental market data"""
        opportunities = data_manager.get_investment_opportunities()
        return json.dumps(opportunities, indent=2)

    @mcp.tool()
    def get_recent_sales() -> str:
        """Get all recent sales transactions"""
        sales = data_manager.get_recent_sales()
        return json.dumps(sales, indent=2)

    @mcp.tool()
    def get_sales_by_area(area: str) -> str:
        """Get recent sales in a specific area"""
        sales = data_manager.get_sales_by_area(area)
        return json.dumps({
            "area": area,
            "sales_count": len(sales),
            "sales": sales
        }, indent=2) 