"""
Agent-related MCP tools
"""

import json
from mcp.server.fastmcp import FastMCP
from utils import data_manager


def register_agent_tools(mcp: FastMCP):
    """Register all agent-related tools with the MCP server"""
    
    @mcp.tool()
    def get_all_agents() -> str:
        """Get all real estate agent profiles"""
        agents = data_manager.get_all_agents()
        return json.dumps(agents, indent=2)

    @mcp.tool()
    def get_agent_details(agent_id: str) -> str:
        """Get detailed information about a specific agent by ID"""
        agent = data_manager.get_agent_by_id(agent_id)
        if agent:
            return json.dumps(agent, indent=2)
        return f"Agent with ID {agent_id} not found"

    @mcp.tool()
    def search_agents(query: str) -> str:
        """Search agents by name, specialization, or expertise area"""
        results = data_manager.search_agents(query)
        return json.dumps({
            "query": query,
            "results_count": len(results),
            "agents": results
        }, indent=2)

    @mcp.tool()
    def get_agent_properties(agent_id: str) -> str:
        """Get all properties handled by a specific agent"""
        properties = data_manager.get_properties_by_agent(agent_id)
        agent = data_manager.get_agent_by_id(agent_id)
        
        return json.dumps({
            "agent_id": agent_id,
            "agent_name": agent.get("name", "Unknown") if agent else "Unknown",
            "properties_count": len(properties),
            "properties": properties
        }, indent=2)

    @mcp.tool()
    def get_agent_sales(agent_id: str) -> str:
        """Get recent sales by a specific agent"""
        sales = data_manager.get_sales_by_agent(agent_id)
        agent = data_manager.get_agent_by_id(agent_id)
        
        return json.dumps({
            "agent_id": agent_id,
            "agent_name": agent.get("name", "Unknown") if agent else "Unknown",
            "sales_count": len(sales),
            "sales": sales
        }, indent=2)

    @mcp.tool()
    def get_agent_clients(agent_id: str) -> str:
        """Get all clients for a specific agent"""
        clients = data_manager.get_clients_by_agent(agent_id)
        agent = data_manager.get_agent_by_id(agent_id)
        
        return json.dumps({
            "agent_id": agent_id,
            "agent_name": agent.get("name", "Unknown") if agent else "Unknown",
            "clients_count": len(clients),
            "clients": clients
        }, indent=2)

    @mcp.tool()
    def get_agent_dashboard(agent_id: str) -> str:
        """Get comprehensive dashboard for an agent including performance metrics"""
        agent = data_manager.get_agent_by_id(agent_id)
        if not agent:
            return f"Agent with ID {agent_id} not found"
        
        properties = data_manager.get_properties_by_agent(agent_id)
        clients = data_manager.get_clients_by_agent(agent_id)
        sales = data_manager.get_sales_by_agent(agent_id)
        
        # Calculate performance metrics
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