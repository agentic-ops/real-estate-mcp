"""
Property resources for the Real Estate MCP Server
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import data_manager


def register_property_resources(mcp: FastMCP):
    """Register all property-related resources with the MCP server"""

    @mcp.resource("realestate://all-properties")
    def get_all_properties_resource() -> str:
        """Complete listing of all active properties"""
        properties = data_manager.get_all_properties()
        return json.dumps(properties, indent=2)

    @mcp.resource("realestate://properties/area/{area}")
    def get_area_properties_resource(area: str) -> str:
        """Properties in a specific area"""
        properties = data_manager.get_properties_by_area(area)
        return json.dumps(
            {
                "area": area,
                "properties_count": len(properties),
                "properties": properties,
            },
            indent=2,
        )

    @mcp.resource("realestate://property/{property_id}/insights")
    def get_property_insights_resource(property_id: str) -> str:
        """Comprehensive property insights including market context"""
        prop = data_manager.get_property_by_id(property_id)
        if not prop:
            return json.dumps(
                {"error": f"Property with ID {property_id} not found"}, indent=2
            )

        area = prop.get("area")
        agent = data_manager.get_agent_by_id(prop.get("agent_id"))
        area_info = data_manager.get_area_info(area)
        area_market = data_manager.get_area_market_data(area)
        comparable_sales = data_manager.get_sales_by_area(area)
        amenities = data_manager.get_area_amenities(area)

        insights = {
            "property": prop,
            "listing_agent": agent,
            "area_context": {
                "area_info": area_info,
                "market_data": area_market,
                "amenities": amenities,
            },
            "comparable_sales": {
                "count": len(comparable_sales),
                "sales": comparable_sales,
            },
        }

        return json.dumps(insights, indent=2)
