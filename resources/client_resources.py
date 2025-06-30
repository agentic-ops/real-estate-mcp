"""
Client resources for the Real Estate MCP Server
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import data_manager


def register_client_resources(mcp: FastMCP):
    """Register all client-related resources with the MCP server"""

    @mcp.resource("realestate://client/{client_id}/matches")
    def get_client_matches_resource(client_id: str) -> str:
        """Properties matching a client's preferences"""
        from utils import PropertyFilter

        client = data_manager.get_client_by_id(client_id)
        if not client:
            return json.dumps(
                {"error": f"Client with ID {client_id} not found"}, indent=2
            )

        if client.get("type") != "Buyer":
            return json.dumps(
                {
                    "client_id": client_id,
                    "client_name": client.get("name"),
                    "message": f"Client is not a buyer (type: {client.get('type')})",
                    "matching_properties": [],
                },
                indent=2,
            )

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
