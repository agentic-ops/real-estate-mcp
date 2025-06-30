"""
Agent resources for the Real Estate MCP Server
"""

import json

from mcp.server.fastmcp import FastMCP

from utils import data_manager


def register_agent_resources(mcp: FastMCP):
    """Register all agent-related resources with the MCP server"""

    @mcp.resource("realestate://all-agents")
    def get_all_agents_resource() -> str:
        """Complete listing of all real estate agents"""
        agents = data_manager.get_all_agents()
        return json.dumps(agents, indent=2)

    @mcp.resource("realestate://agent/{agent_id}/dashboard")
    def get_agent_dashboard_resource(agent_id: str) -> str:
        """Agent dashboard with performance metrics and listings"""
        agent = data_manager.get_agent_by_id(agent_id)
        if not agent:
            return json.dumps(
                {"error": f"Agent with ID {agent_id} not found"}, indent=2
            )

        properties = data_manager.get_properties_by_agent(agent_id)
        clients = data_manager.get_clients_by_agent(agent_id)
        sales = data_manager.get_sales_by_agent(agent_id)

        recent_sales = agent.get("recent_sales", [])
        total_sales_volume = sum(sale.get("sale_price", 0) for sale in recent_sales)
        avg_days_on_market = (
            sum(sale.get("days_on_market", 0) for sale in recent_sales)
            / len(recent_sales)
            if recent_sales
            else 0
        )

        dashboard = {
            "agent_info": agent,
            "performance_metrics": {
                "active_listings": len(properties),
                "total_clients": len(clients),
                "recent_sales_count": len(recent_sales),
                "total_sales_volume": total_sales_volume,
                "avg_days_on_market": avg_days_on_market,
            },
            "active_listings": properties,
            "clients": clients,
            "recent_sales": sales,
        }

        return json.dumps(dashboard, indent=2)
