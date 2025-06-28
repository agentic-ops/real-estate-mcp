"""
Property-related MCP tools
"""

import json
from typing import Optional
from mcp.server.fastmcp import FastMCP
from utils import data_manager, PropertyFilter


def register_property_tools(mcp: FastMCP):
    """Register all property-related tools with the MCP server"""
    
    @mcp.tool()
    def get_all_properties() -> str:
        """Get all active property listings"""
        properties = data_manager.get_all_properties()
        return json.dumps(properties, indent=2)

    @mcp.tool()
    def get_property_details(property_id: str) -> str:
        """Get detailed information about a specific property by ID"""
        property_data = data_manager.get_property_by_id(property_id)
        if property_data:
            return json.dumps(property_data, indent=2)
        return f"Property with ID {property_id} not found"

    @mcp.tool()
    def search_properties(query: str) -> str:
        """Search properties by text query (address, description, features, etc.)"""
        results = data_manager.search_properties(query)
        return json.dumps({
            "query": query,
            "results_count": len(results),
            "properties": results
        }, indent=2)

    @mcp.tool()
    def filter_properties(
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        min_bedrooms: Optional[int] = None,
        max_bedrooms: Optional[int] = None,
        areas: Optional[str] = None,
        property_types: Optional[str] = None
    ) -> str:
        """Filter properties by criteria. Areas and property_types should be comma-separated strings."""
        filters = PropertyFilter(
            min_price=min_price,
            max_price=max_price,
            min_bedrooms=min_bedrooms,
            max_bedrooms=max_bedrooms,
            areas=areas.split(",") if areas else None,
            property_types=property_types.split(",") if property_types else None
        )
        
        results = data_manager.filter_properties(filters)
        return json.dumps({
            "filters_applied": {
                "min_price": min_price,
                "max_price": max_price,
                "min_bedrooms": min_bedrooms,
                "max_bedrooms": max_bedrooms,
                "areas": areas.split(",") if areas else None,
                "property_types": property_types.split(",") if property_types else None
            },
            "results_count": len(results),
            "properties": results
        }, indent=2)

    @mcp.tool()
    def get_properties_by_area(area: str) -> str:
        """Get all properties in a specific area"""
        properties = data_manager.get_properties_by_area(area)
        return json.dumps({
            "area": area,
            "properties_count": len(properties),
            "properties": properties
        }, indent=2)

    @mcp.tool()
    def get_property_insights(property_id: str) -> str:
        """Get comprehensive insights for a property including market context and comparables"""
        prop = data_manager.get_property_by_id(property_id)
        if not prop:
            return f"Property with ID {property_id} not found"
        
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
                "amenities": amenities
            },
            "comparable_sales": {
                "count": len(comparable_sales),
                "sales": comparable_sales
            }
        }
        
        return json.dumps(insights, indent=2) 