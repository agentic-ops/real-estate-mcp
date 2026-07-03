"""Integration tests for the optional live-data adapters.

All tests are network-free: real HTTP is replaced with
``httpx.MockTransport`` so no external calls are ever made. This mirrors the
production default where integrations are OFF.
"""

import httpx

from integrations.census import CensusClient
from integrations.config import (
    CensusSettings,
    RentCastSettings,
    get_integration_settings,
)
from integrations.rentcast import RentCastClient
from tests.conftest import call_tool_json


def _mock_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


class TestDefaultsOff:
    def test_settings_default_disabled(self, monkeypatch):
        for name in (
            "CENSUS_ENABLED",
            "RENTCAST_ENABLED",
            "RENTCAST_API_KEY",
            "CENSUS_API_KEY",
        ):
            monkeypatch.delenv(name, raising=False)
        settings = get_integration_settings()
        assert settings.census.enabled is False
        assert settings.rentcast.enabled is False

    def test_disabled_census_makes_no_call(self, monkeypatch):
        monkeypatch.delenv("CENSUS_ENABLED", raising=False)

        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = CensusClient(
            CensusSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.demographics("06")
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_rentcast_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = RentCastClient(
            RentCastSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.lookup_property("1 Main St")
        assert result["enabled"] is False
        assert result["results"] == []


class TestStatusNeverLeaksSecrets:
    def test_rentcast_status_hides_key(self):
        settings = RentCastSettings(enabled=True, api_key="super-secret-token")
        status = RentCastClient(settings).status()
        assert "super-secret-token" not in str(status)
        assert status["configured"] is True

    def test_census_status_hides_key(self):
        settings = CensusSettings(enabled=True, api_key="secret-key")
        status = CensusClient(settings).status()
        assert "secret-key" not in str(status)
        assert status["has_api_key"] is True


class TestEnabledWithMock:
    def test_census_parses_rows(self):
        def handler(request):
            assert "census.gov" in str(request.url)
            payload = [
                ["NAME", "B01003_001E", "B19013_001E", "state"],
                ["California", "39000000", "84000", "06"],
            ]
            return httpx.Response(200, json=payload)

        client = CensusClient(
            CensusSettings(enabled=True), http_client=_mock_client(handler)
        )
        result = client.demographics("06")
        assert result["enabled"] is True
        assert result["result_count"] == 1
        assert result["results"][0]["NAME"] == "California"

    def test_rentcast_requires_key(self):
        client = RentCastClient(RentCastSettings(enabled=True, api_key=None))
        result = client.lookup_property("1 Main St")
        assert "RENTCAST_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_rentcast_parses_results(self):
        def handler(request):
            assert request.headers.get("X-Api-Key") == "key123"
            return httpx.Response(200, json=[{"id": "abc", "price": 500000}])

        client = RentCastClient(
            RentCastSettings(enabled=True, api_key="key123"),
            http_client=_mock_client(handler),
        )
        result = client.lookup_property("1 Main St")
        assert result["enabled"] is True
        assert result["result_count"] == 1
        assert result["results"][0]["id"] == "abc"


class TestIntegrationTools:
    async def test_integration_status_tool(self, mcp_server):
        result = await call_tool_json(mcp_server, "integration_status", {})
        assert "census" in result
        assert "rentcast" in result

    async def test_lookup_live_property_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("RENTCAST_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "lookup_live_property", {"address": "1 Main St"}
        )
        assert result["enabled"] is False

    async def test_get_live_demographics_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("CENSUS_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_demographics", {"state_fips": "06"}
        )
        assert result["enabled"] is False
