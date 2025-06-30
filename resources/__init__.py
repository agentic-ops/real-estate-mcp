"""Resources module for the Real Estate MCP Server"""

from .agent_resources import register_agent_resources
from .client_resources import register_client_resources
from .location_resources import register_location_resources
from .market_resources import register_market_resources
from .property_resources import register_property_resources

__all__ = [
    "register_agent_resources",
    "register_client_resources",
    "register_location_resources",
    "register_market_resources",
    "register_property_resources",
]
