"""Tools for optional live data integrations.

Free sources: Census, Walk Score, FEMA, FRED, FBI Crime Data, EPA, NOAA.
Paid/metered sources: RentCast, Zillow.

These tools expose the feature-flagged integrations to MCP clients. They
are safe to call even when integrations are disabled: in that case they
return a clear status payload and make no network requests.
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

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
            "walkscore": WalkScoreClient(settings.walkscore).status(),
            "fema": FemaClient(settings.fema).status(),
            "fred": FredClient(settings.fred).status(),
            "fbi_crime": FbiCrimeClient(settings.fbi_crime).status(),
            "epa": EpaClient(settings.epa).status(),
            "noaa": NoaaClient(settings.noaa).status(),
            "rentcast": RentCastClient(settings.rentcast).status(),
            "zillow": ZillowClient(settings.zillow).status(),
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
    def lookup_live_zestimate(address: str) -> str:
        """Look up a live Zillow-style valuation (Zestimate) when enabled.

        Disabled by default -- Zillow requires an approved, paid data
        license (e.g. Bridge Interactive); returns a status payload
        explaining how to enable it.
        """
        audit("lookup_live_zestimate", address=address)
        settings = get_integration_settings()
        result = ZillowClient(settings.zillow).lookup_zestimate(address)
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

    @mcp.tool()
    def get_live_walk_score(address: str, lat: float, lon: float) -> str:
        """Fetch live Walk/Transit/Bike Score for a location when enabled.

        Disabled by default -- returns a status payload explaining how to
        enable the free-tier Walk Score integration.
        """
        audit("get_live_walk_score", address=address, lat=lat, lon=lon)
        settings = get_integration_settings()
        result = WalkScoreClient(settings.walkscore).walk_score(address, lat, lon)
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_flood_zone(lat: float, lon: float) -> str:
        """Fetch the live FEMA flood hazard zone for a coordinate when enabled.

        Disabled by default -- returns a status payload explaining how to
        enable the free FEMA integration.
        """
        audit("get_live_flood_zone", lat=lat, lon=lon)
        settings = get_integration_settings()
        result = FemaClient(settings.fema).flood_zone(lat, lon)
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_mortgage_rate() -> str:
        """Fetch the latest weekly Freddie Mac 30-year mortgage rate (FRED).

        Disabled by default -- returns a status payload explaining how to
        enable the free FRED integration.
        """
        audit("get_live_mortgage_rate")
        settings = get_integration_settings()
        result = FredClient(settings.fred).current_mortgage_rate_30yr()
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_crime_summary(state_abbr: str, offense: str = "violent-crime") -> str:
        """Fetch live FBI crime statistics for a state when enabled.

        Disabled by default -- returns a status payload explaining how to
        enable the free FBI Crime Data integration.
        """
        audit("get_live_crime_summary", state_abbr=state_abbr, offense=offense)
        settings = get_integration_settings()
        result = FbiCrimeClient(settings.fbi_crime).state_crime_summary(
            state_abbr, offense=offense
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_environmental_hazards(state_abbr: str) -> str:
        """Fetch live EPA-reported environmental hazards for a state.

        Disabled by default -- returns a status payload explaining how to
        enable the free EPA Envirofacts integration.
        """
        audit("get_live_environmental_hazards", state_abbr=state_abbr)
        settings = get_integration_settings()
        result = EpaClient(settings.epa).environmental_hazards_by_state(state_abbr)
        return json.dumps(result, indent=2)

    @mcp.tool()
    def get_live_weather_forecast(lat: float, lon: float) -> str:
        """Fetch the live NOAA/NWS weather forecast for a coordinate.

        Disabled by default -- returns a status payload explaining how to
        enable the free NOAA integration.
        """
        audit("get_live_weather_forecast", lat=lat, lon=lon)
        settings = get_integration_settings()
        result = NoaaClient(settings.noaa).forecast(lat, lon)
        return json.dumps(result, indent=2)
