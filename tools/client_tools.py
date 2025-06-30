"""
Client management MCP tools
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import PropertyFilter, data_manager


def register_client_tools(mcp: FastMCP):
    """Register all client management tools with the MCP server"""

    @mcp.tool()
    def get_all_clients() -> str:
        """Get all client information"""
        clients = data_manager.get_all_clients()
        return json.dumps(clients, indent=2)

    @mcp.tool()
    def get_client_details(client_id: str) -> str:
        """Get detailed information about a specific client by ID"""
        client = data_manager.get_client_by_id(client_id)
        if client:
            return json.dumps(client, indent=2)
        return f"Client with ID {client_id} not found"

    @mcp.tool()
    def match_client_preferences(client_id: str) -> str:
        """Match properties to a client's preferences and budget"""
        client = data_manager.get_client_by_id(client_id)
        if not client:
            return f"Client with ID {client_id} not found"

        if client.get("type") != "Buyer":
            return f"Client {client_id} is not a buyer (type: {client.get('type')})"

        preferences = client.get("preferences", {})
        budget = preferences.get("budget_range", {})

        filters = PropertyFilter(
            min_price=budget.get("min"),
            max_price=budget.get("max"),
            areas=preferences.get("desired_areas"),
            property_types=(
                [preferences.get("property_type")]
                if preferences.get("property_type")
                else None
            ),
        )

        matching_properties = data_manager.filter_properties(filters)

        return json.dumps(
            {
                "client_id": client_id,
                "client_name": client.get("name"),
                "preferences": preferences,
                "matching_properties_count": len(matching_properties),
                "matching_properties": matching_properties,
            },
            indent=2,
        )
