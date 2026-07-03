"""Resources describing the optional live-data integrations."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from integrations import CensusClient, RentCastClient, get_integration_settings
from utils import audit


def register_integration_resources(mcp: FastMCP) -> None:
    """Register integration-status resources with the MCP server."""

    @mcp.resource("realestate://integrations/status")
    def integrations_status_resource() -> str:
        """Report enabled/configured state of all live integrations (no secrets)."""
        audit("resource_integrations_status")
        settings = get_integration_settings()
        return json.dumps(
            {
                "census": CensusClient(settings.census).status(),
                "rentcast": RentCastClient(settings.rentcast).status(),
            },
            indent=2,
        )
