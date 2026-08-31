"""Resources describing the optional live-data integrations."""

from __future__ import annotations

import json

from mcp.server.mcpserver import MCPServer

from integrations import (
    CensusClient,
    EpaClient,
    FbiCrimeClient,
    FemaClient,
    FredClient,
    NoaaClient,
    RentCastClient,
    WalkScoreClient,
    ZillowClient,
    get_integration_settings,
)
from utils import audit


def register_integration_resources(mcp: MCPServer) -> None:
    """Register integration-status resources with the MCP server."""

    @mcp.resource("realestate://integrations/status")
    def integrations_status_resource() -> str:
        """Report enabled/configured state of all live integrations (no secrets)."""
        audit("resource_integrations_status")
        settings = get_integration_settings()
        return json.dumps(
            {
                "census": CensusClient(settings.census).status(),
                "walkscore": WalkScoreClient(settings.walkscore).status(),
                "fema": FemaClient(settings.fema).status(),
                "fred": FredClient(settings.fred).status(),
                "fbi_crime": FbiCrimeClient(settings.fbi_crime).status(),
                "epa": EpaClient(settings.epa).status(),
                "noaa": NoaaClient(settings.noaa).status(),
                "rentcast": RentCastClient(settings.rentcast).status(),
                "zillow": ZillowClient(settings.zillow).status(),
            },
            indent=2,
        )
