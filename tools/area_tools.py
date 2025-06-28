"""
Area and amenities MCP tools
"""

import json
from mcp.server.fastmcp import FastMCP
from utils import data_manager


def register_area_tools(mcp: FastMCP):
    """Register all area and amenities tools with the MCP server"""
    
    @mcp.tool()
    def get_all_areas() -> str:
        """Get information about all areas in the city"""
        areas = data_manager.get_all_areas()
        return json.dumps(areas, indent=2)

    @mcp.tool()
    def get_area_details(area_name: str) -> str:
        """Get detailed information about a specific area"""
        area_info = data_manager.get_area_info(area_name)
        if area_info:
            return json.dumps(area_info, indent=2)
        return f"Area '{area_name}' not found"

    @mcp.tool()
    def get_city_overview() -> str:
        """Get overall city information and demographics"""
        overview = data_manager.get_city_overview()
        return json.dumps(overview, indent=2)

    @mcp.tool()
    def get_area_amenities(area: str) -> str:
        """Get amenities (schools, parks, shopping) for a specific area"""
        amenities = data_manager.get_area_amenities(area)
        return json.dumps({
            "area": area,
            "amenities": amenities
        }, indent=2)

    @mcp.tool()
    def get_schools_data() -> str:
        """Get all schools information including ratings and programs"""
        schools = data_manager.amenities.get("schools", {})
        return json.dumps(schools, indent=2)

    @mcp.tool()
    def get_parks_and_recreation() -> str:
        """Get parks and recreation facilities information"""
        parks_rec = data_manager.amenities.get("parks_and_recreation", {})
        return json.dumps(parks_rec, indent=2)

    @mcp.tool()
    def get_shopping_amenities() -> str:
        """Get shopping centers and retail information"""
        shopping = data_manager.amenities.get("shopping", {})
        return json.dumps(shopping, indent=2)

    @mcp.tool()
    def get_healthcare_facilities() -> str:
        """Get healthcare facilities and medical services"""
        healthcare = data_manager.amenities.get("healthcare", {})
        return json.dumps(healthcare, indent=2)

    @mcp.tool()
    def get_comprehensive_area_report(area: str) -> str:
        """Get a comprehensive report for an area including properties, market data, and amenities"""
        # Get area info
        area_info = data_manager.get_area_info(area)
        market_data = data_manager.get_area_market_data(area)
        properties = data_manager.get_properties_by_area(area)
        sales = data_manager.get_sales_by_area(area)
        amenities = data_manager.get_area_amenities(area)
        
        report = {
            "area": area,
            "area_info": area_info,
            "market_data": market_data,
            "active_properties": {
                "count": len(properties),
                "properties": properties
            },
            "recent_sales": {
                "count": len(sales),
                "sales": sales
            },
            "amenities": amenities
        }
        
        return json.dumps(report, indent=2) 