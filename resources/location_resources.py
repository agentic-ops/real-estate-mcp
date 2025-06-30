"""
Location resources for the Real Estate MCP Server
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import data_manager


def register_location_resources(mcp: FastMCP):
    """Register all location-related resources with the MCP server"""

    @mcp.resource("realestate://all-areas")
    def get_all_areas_resource() -> str:
        """Information about all areas in the city"""
        areas = data_manager.get_all_areas()
        return json.dumps(areas, indent=2)

    @mcp.resource("realestate://amenities")
    def get_amenities_resource() -> str:
        """All amenities data including schools, parks, shopping, healthcare"""
        return json.dumps(data_manager.amenities, indent=2)
