"""
Static resources for the Real Estate MCP Server
"""

import json
from mcp.server.fastmcp import FastMCP
from utils import data_manager


def register_static_resources(mcp: FastMCP):
    """Register all static resources with the MCP server"""
    
    @mcp.resource("realestate://all-properties")
    def get_all_properties_resource() -> str:
        """Complete listing of all active properties"""
        properties = data_manager.get_all_properties()
        return json.dumps(properties, indent=2)

    @mcp.resource("realestate://all-agents")
    def get_all_agents_resource() -> str:
        """Complete listing of all real estate agents"""
        agents = data_manager.get_all_agents()
        return json.dumps(agents, indent=2)

    @mcp.resource("realestate://market-overview")
    def get_market_overview_resource() -> str:
        """Current market overview and trends"""
        overview = data_manager.get_market_overview()
        return json.dumps(overview, indent=2)

    @mcp.resource("realestate://all-areas")
    def get_all_areas_resource() -> str:
        """Information about all areas in the city"""
        areas = data_manager.get_all_areas()
        return json.dumps(areas, indent=2)

    @mcp.resource("realestate://amenities")
    def get_amenities_resource() -> str:
        """All amenities data including schools, parks, shopping, healthcare"""
        return json.dumps(data_manager.amenities, indent=2) 