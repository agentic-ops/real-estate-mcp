"""MCP tool modules for the Real Estate MCP Server.

``register_all_tools`` registers every *enabled* tool category with the
server. Categories are toggled via ``REALESTATE_MCP_ENABLE_*`` environment
variables (see :mod:`feature_flags`); all default to enabled.
"""

from __future__ import annotations

from feature_flags import is_category_enabled
from tools.agent_tools import register_agent_tools
from tools.analysis_queue_tools import register_analysis_queue_tools
from tools.area_tools import register_area_tools
from tools.client_tools import register_client_tools
from tools.deep_analysis_tools import register_deep_analysis_tools
from tools.document_tools import register_document_tools
from tools.integration_tools import register_integration_tools
from tools.market_tools import register_market_tools
from tools.mortgage_tools import register_mortgage_tools
from tools.property_tools import register_property_tools
from tools.system_tools import register_system_tools
from tools.valuation_tools import register_valuation_tools


def register_all_tools(mcp) -> None:
    """Register every enabled tool category with the MCP server."""

    if is_category_enabled("property"):
        register_property_tools(mcp)
    if is_category_enabled("agent"):
        register_agent_tools(mcp)
    if is_category_enabled("market"):
        register_market_tools(mcp)
    if is_category_enabled("client"):
        register_client_tools(mcp)
    if is_category_enabled("area"):
        register_area_tools(mcp)
    if is_category_enabled("mortgage"):
        register_mortgage_tools(mcp)
    if is_category_enabled("valuation"):
        register_valuation_tools(mcp)
        register_deep_analysis_tools(mcp)
    if is_category_enabled("document"):
        register_document_tools(mcp)
    if is_category_enabled("analysis_queue"):
        register_analysis_queue_tools(mcp)
    if is_category_enabled("integrations"):
        register_integration_tools(mcp)
    if is_category_enabled("system"):
        register_system_tools(mcp)


__all__ = [
    "register_all_tools",
    "register_property_tools",
    "register_agent_tools",
    "register_market_tools",
    "register_client_tools",
    "register_area_tools",
    "register_mortgage_tools",
    "register_valuation_tools",
    "register_deep_analysis_tools",
    "register_document_tools",
    "register_analysis_queue_tools",
    "register_integration_tools",
    "register_system_tools",
]
