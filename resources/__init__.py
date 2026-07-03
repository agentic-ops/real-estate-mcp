"""Resource modules for the Real Estate MCP Server.

``register_all_resources`` registers the always-on configuration resource
plus every enabled domain's resources (gated by the same
``REALESTATE_MCP_ENABLE_*`` feature flags as the tools).
"""

from __future__ import annotations

from feature_flags import is_category_enabled

from .agent_resources import register_agent_resources
from .client_resources import register_client_resources
from .config_resources import register_config_resources
from .integration_resources import register_integration_resources
from .location_resources import register_location_resources
from .market_resources import register_market_resources
from .property_resources import register_property_resources


def register_all_resources(mcp) -> None:
    """Register every enabled resource domain with the MCP server."""

    register_config_resources(mcp)
    if is_category_enabled("property"):
        register_property_resources(mcp)
    if is_category_enabled("agent"):
        register_agent_resources(mcp)
    if is_category_enabled("market"):
        register_market_resources(mcp)
    if is_category_enabled("client"):
        register_client_resources(mcp)
    if is_category_enabled("area"):
        register_location_resources(mcp)
    if is_category_enabled("integrations"):
        register_integration_resources(mcp)


__all__ = [
    "register_all_resources",
    "register_config_resources",
    "register_integration_resources",
    "register_agent_resources",
    "register_client_resources",
    "register_location_resources",
    "register_market_resources",
    "register_property_resources",
]
