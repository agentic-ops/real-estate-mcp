"""Category-level feature flags for Real Estate MCP Server tool groups.

Every tool category is enabled by default. Set the corresponding
``REALESTATE_MCP_ENABLE_*`` environment variable to ``false`` to disable an
entire category (its tools and matching resources will not be registered).

This lets operators trim the surface area of the server -- for example
disabling the optional live ``integrations`` category, or the SQLite-backed
``analysis_queue`` -- without touching code.
"""

from __future__ import annotations

import os
from typing import Dict, List

TOOL_CATEGORIES: Dict[str, str] = {
    "property": "REALESTATE_MCP_ENABLE_PROPERTY",
    "agent": "REALESTATE_MCP_ENABLE_AGENT",
    "market": "REALESTATE_MCP_ENABLE_MARKET",
    "client": "REALESTATE_MCP_ENABLE_CLIENT",
    "area": "REALESTATE_MCP_ENABLE_AREA",
    "mortgage": "REALESTATE_MCP_ENABLE_MORTGAGE",
    "valuation": "REALESTATE_MCP_ENABLE_VALUATION",
    "document": "REALESTATE_MCP_ENABLE_DOCUMENT",
    "analysis_queue": "REALESTATE_MCP_ENABLE_ANALYSIS_QUEUE",
    "integrations": "REALESTATE_MCP_ENABLE_INTEGRATIONS",
    "system": "REALESTATE_MCP_ENABLE_SYSTEM",
}


def _bool_env(name: str, default: bool = True) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def is_category_enabled(category: str) -> bool:
    """Return whether a tool category is enabled."""

    env_name = TOOL_CATEGORIES.get(category)
    if env_name is None:
        raise KeyError(f"Unknown tool category: {category}")
    return _bool_env(env_name, default=True)


def enabled_categories() -> Dict[str, bool]:
    """Return the enabled/disabled state of every tool category."""

    return {category: is_category_enabled(category) for category in TOOL_CATEGORIES}


def disabled_categories() -> List[str]:
    """Return names of categories that are currently disabled."""

    return [name for name, enabled in enabled_categories().items() if not enabled]
