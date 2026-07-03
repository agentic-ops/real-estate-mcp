"""Tools for optional live data integrations (Census, RentCast).

These tools expose the feature-flagged integrations to MCP clients. They
are safe to call even when integrations are disabled: in that case they
return a clear status payload and make no network requests.
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from integrations import (
    CensusClient,
    RentCastClient,
    get_integration_settings,
)
from utils import audit


def register_integration_tools(mcp: FastMCP) -> None:
    """Register live-integration tools with the MCP server."""

    @mcp.tool()
    def integration_status() -> str:
        """Report which live integrations are enabled/configured.

        Reads the current feature flags and credential presence. Never
        returns secret values -- only booleans and non-sensitive metadata.
        """
        audit("integration_status")
        settings = get_integration_settings()
        report = {
            "census": CensusClient(settings.census).status(),
            "rentcast": RentCastClient(settings.rentcast).status(),
        }
        return json.dumps(report, indent=2)

    @mcp.tool()
    def lookup_live_property(address: str) -> str:
        """Look up live property records via RentCast when enabled.

        Disabled by default -- returns a status payload explaining how to
        enable the integration (may incur metered API costs).
        """
        audit("lookup_live_property", address=address)
        settings = get_integration_settings()
        result = RentCastClient(settings.rentcast).lookup_property(address)
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_demographics(state_fips: str, year: int = 2022) -> str:
        """Fetch live Census demographics for a state FIPS code when enabled.

        Disabled by default -- returns a status payload explaining how to
        enable the free Census integration.
        """
        audit("get_live_demographics", state_fips=state_fips, year=year)
        settings = get_integration_settings()
        result = CensusClient(settings.census).demographics(state_fips, year=year)
        return json.dumps(result, indent=2)
