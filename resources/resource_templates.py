"""
Resource templates for the Real Estate MCP Server
"""

import json
from mcp.server.fastmcp import FastMCP
from utils import data_manager


def register_resource_templates(mcp: FastMCP):
    """Register all resource templates with the MCP server"""
    
    @mcp.resource("realestate://properties/area/{area}")
    def get_area_properties_resource(area: str) -> str:
        """Properties in a specific area"""
        properties = data_manager.get_properties_by_area(area)
        return json.dumps({
            "area": area,
            "properties_count": len(properties),
            "properties": properties
        }, indent=2)

    @mcp.resource("realestate://agent/{agent_id}/dashboard")
    def get_agent_dashboard_resource(agent_id: str) -> str:
        """Agent dashboard with performance metrics and listings"""
        agent = data_manager.get_agent_by_id(agent_id)
        if not agent:
            return json.dumps({"error": f"Agent with ID {agent_id} not found"}, indent=2)
        
        properties = data_manager.get_properties_by_agent(agent_id)
        clients = data_manager.get_clients_by_agent(agent_id)
        sales = data_manager.get_sales_by_agent(agent_id)
        
        recent_sales = agent.get("recent_sales", [])
        total_sales_volume = sum(sale.get("sale_price", 0) for sale in recent_sales)
        avg_days_on_market = sum(sale.get("days_on_market", 0) for sale in recent_sales) / len(recent_sales) if recent_sales else 0
        
        dashboard = {
            "agent_info": agent,
            "performance_metrics": {
                "active_listings": len(properties),
                "total_clients": len(clients),
                "recent_sales_count": len(recent_sales),
                "total_sales_volume": total_sales_volume,
                "avg_days_on_market": avg_days_on_market
            },
            "active_listings": properties,
            "clients": clients,
            "recent_sales": sales
        }
        
        return json.dumps(dashboard, indent=2)

    @mcp.resource("realestate://market/area/{area}")
    def get_area_market_resource(area: str) -> str:
        """Market analysis for a specific area"""
        market_data = data_manager.get_area_market_data(area)
        area_info = data_manager.get_area_info(area)
        sales = data_manager.get_sales_by_area(area)
        
        return json.dumps({
            "area": area,
            "area_info": area_info,
            "market_data": market_data,
            "recent_sales_count": len(sales),
            "recent_sales": sales
        }, indent=2)

    @mcp.resource("realestate://property/{property_id}/insights")
    def get_property_insights_resource(property_id: str) -> str:
        """Comprehensive property insights including market context"""
        prop = data_manager.get_property_by_id(property_id)
        if not prop:
            return json.dumps({"error": f"Property with ID {property_id} not found"}, indent=2)
        
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

    @mcp.resource("realestate://client/{client_id}/matches")
    def get_client_matches_resource(client_id: str) -> str:
        """Properties matching a client's preferences"""
        from utils import PropertyFilter
        
        client = data_manager.get_client_by_id(client_id)
        if not client:
            return json.dumps({"error": f"Client with ID {client_id} not found"}, indent=2)
        
        if client.get("type") != "Buyer":
            return json.dumps({
                "client_id": client_id,
                "client_name": client.get("name"),
                "message": f"Client is not a buyer (type: {client.get('type')})",
                "matching_properties": []
            }, indent=2)
        
        preferences = client.get("preferences", {})
        budget = preferences.get("budget_range", {})
        
        filters = PropertyFilter(
            min_price=budget.get("min"),
            max_price=budget.get("max"),
            areas=preferences.get("desired_areas"),
            property_types=[preferences.get("property_type")] if preferences.get("property_type") else None
        )
        
        matching_properties = data_manager.filter_properties(filters)
        
        return json.dumps({
            "client_id": client_id,
            "client_name": client.get("name"),
            "preferences": preferences,
            "matching_properties_count": len(matching_properties),
            "matching_properties": matching_properties
        }, indent=2) 