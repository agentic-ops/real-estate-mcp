"""Integration tests for the optional live-data adapters.

All tests are network-free: real HTTP is replaced with
``httpx.MockTransport`` so no external calls are ever made. This mirrors the
production default where integrations are OFF.
"""

import httpx

from integrations.census import CensusClient
from integrations.config import (
    CensusSettings,
    EpaSettings,
    FbiCrimeSettings,
    FemaSettings,
    FredSettings,
    NoaaSettings,
    RentCastSettings,
    WalkScoreSettings,
    ZillowSettings,
    get_integration_settings,
)
from integrations.epa import EpaClient
from integrations.fbi_crime import FbiCrimeClient
from integrations.fema import FemaClient
from integrations.fred import FredClient
from integrations.noaa import NoaaClient
from integrations.rentcast import RentCastClient
from integrations.walkscore import WalkScoreClient
from integrations.zillow import ZillowClient
from tests.conftest import call_tool_json

ALL_ENV_FLAGS = (
    "CENSUS_ENABLED",
    "CENSUS_API_KEY",
    "RENTCAST_ENABLED",
    "RENTCAST_API_KEY",
    "WALKSCORE_ENABLED",
    "WALKSCORE_API_KEY",
    "FEMA_ENABLED",
    "FRED_ENABLED",
    "FRED_API_KEY",
    "FBI_CRIME_ENABLED",
    "FBI_CRIME_API_KEY",
    "EPA_ENABLED",
    "NOAA_ENABLED",
    "ZILLOW_ENABLED",
    "ZILLOW_API_KEY",
)


def _mock_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


class TestDefaultsOff:
    def test_settings_default_disabled(self, monkeypatch):
        for name in ALL_ENV_FLAGS:
            monkeypatch.delenv(name, raising=False)
        settings = get_integration_settings()
        assert settings.census.enabled is False
        assert settings.rentcast.enabled is False
        assert settings.walkscore.enabled is False
        assert settings.fema.enabled is False
        assert settings.fred.enabled is False
        assert settings.fbi_crime.enabled is False
        assert settings.epa.enabled is False
        assert settings.noaa.enabled is False
        assert settings.zillow.enabled is False

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

    def test_disabled_walkscore_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = WalkScoreClient(
            WalkScoreSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.walk_score("1 Main St", 47.6, -122.3)
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_fema_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = FemaClient(
            FemaSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.flood_zone(32.3, -96.6)
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_fred_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = FredClient(
            FredSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.current_mortgage_rate_30yr()
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_fbi_crime_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = FbiCrimeClient(
            FbiCrimeSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.state_crime_summary("CA")
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_epa_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = EpaClient(
            EpaSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.environmental_hazards_by_state("CA")
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_noaa_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = NoaaClient(
            NoaaSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.forecast(38.9, -77.0)
        assert result["enabled"] is False
        assert result["results"] == []

    def test_disabled_zillow_makes_no_call(self):
        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted while disabled")

        client = ZillowClient(
            ZillowSettings(enabled=False), http_client=_mock_client(handler)
        )
        result = client.lookup_zestimate("1 Main St")
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
        assert status["configured"] is True

    def test_walkscore_status_hides_key(self):
        settings = WalkScoreSettings(enabled=True, api_key="ws-secret")
        status = WalkScoreClient(settings).status()
        assert "ws-secret" not in str(status)
        assert status["configured"] is True

    def test_fred_status_hides_key(self):
        settings = FredSettings(enabled=True, api_key="fred-secret")
        status = FredClient(settings).status()
        assert "fred-secret" not in str(status)
        assert status["configured"] is True

    def test_fbi_crime_status_hides_key(self):
        settings = FbiCrimeSettings(enabled=True, api_key="fbi-secret")
        status = FbiCrimeClient(settings).status()
        assert "fbi-secret" not in str(status)
        assert status["configured"] is True

    def test_zillow_status_hides_key(self):
        settings = ZillowSettings(enabled=True, api_key="zillow-secret")
        status = ZillowClient(settings).status()
        assert "zillow-secret" not in str(status)
        assert status["configured"] is True

    def test_fema_status_is_always_configured(self):
        status = FemaClient(FemaSettings(enabled=True)).status()
        assert status["configured"] is True
        assert status["missing_settings"] == []

    def test_epa_status_is_always_configured(self):
        status = EpaClient(EpaSettings(enabled=True)).status()
        assert status["configured"] is True

    def test_noaa_status_is_always_configured(self):
        status = NoaaClient(NoaaSettings(enabled=True)).status()
        assert status["configured"] is True


class TestEnabledWithMock:
    def test_census_requires_key(self):
        """Census now requires a key for every request (verified live);
        without one, the client must not attempt a network call."""

        def handler(request):  # pragma: no cover - must never run
            raise AssertionError("network call attempted without a key")

        client = CensusClient(
            CensusSettings(enabled=True, api_key=None),
            http_client=_mock_client(handler),
        )
        result = client.demographics("06")
        assert "CENSUS_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_census_parses_rows(self):
        def handler(request):
            assert "census.gov" in str(request.url)
            assert request.url.params.get("key") == "censuskey"
            payload = [
                ["NAME", "B01003_001E", "B19013_001E", "state"],
                ["California", "39000000", "84000", "06"],
            ]
            return httpx.Response(200, json=payload)

        client = CensusClient(
            CensusSettings(enabled=True, api_key="censuskey"),
            http_client=_mock_client(handler),
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

    def test_walkscore_requires_key(self):
        client = WalkScoreClient(WalkScoreSettings(enabled=True, api_key=None))
        result = client.walk_score("1 Main St", 47.6, -122.3)
        assert "WALKSCORE_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_walkscore_parses_result(self):
        def handler(request):
            assert request.url.params.get("wsapikey") == "wskey"
            return httpx.Response(
                200,
                json={"status": 1, "walkscore": 88, "description": "Very Walkable"},
            )

        client = WalkScoreClient(
            WalkScoreSettings(enabled=True, api_key="wskey"),
            http_client=_mock_client(handler),
        )
        result = client.walk_score("1 Main St", 47.6, -122.3)
        assert result["enabled"] is True
        assert result["results"][0]["walkscore"] == 88

    def test_walkscore_surfaces_error_status_on_http_200(self):
        """Walk Score returns HTTP 200 even for an invalid key (status=40);
        this must be surfaced as an error, not a false success."""

        def handler(request):
            return httpx.Response(200, json={"status": 40})

        client = WalkScoreClient(
            WalkScoreSettings(enabled=True, api_key="bad-key"),
            http_client=_mock_client(handler),
        )
        result = client.walk_score("1 Main St", 47.6, -122.3)
        assert result["enabled"] is True
        assert "40" in result["error"]
        assert result["results"] == []

    def test_fema_parses_features(self):
        def handler(request):
            assert "hazards.fema.gov" in str(request.url)
            payload = {"features": [{"attributes": {"FLD_ZONE": "X"}}]}
            return httpx.Response(200, json=payload)

        client = FemaClient(
            FemaSettings(enabled=True), http_client=_mock_client(handler)
        )
        result = client.flood_zone(32.333, -96.6666)
        assert result["enabled"] is True
        assert result["result_count"] == 1
        assert result["results"][0]["FLD_ZONE"] == "X"

    def test_fred_requires_key(self):
        client = FredClient(FredSettings(enabled=True, api_key=None))
        result = client.current_mortgage_rate_30yr()
        assert "FRED_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_fred_parses_latest_rate(self):
        def handler(request):
            assert request.url.params.get("api_key") == "fredkey"
            payload = {"observations": [{"date": "2026-07-02", "value": "6.85"}]}
            return httpx.Response(200, json=payload)

        client = FredClient(
            FredSettings(enabled=True, api_key="fredkey"),
            http_client=_mock_client(handler),
        )
        result = client.current_mortgage_rate_30yr()
        assert result["enabled"] is True
        assert result["latest_rate_percent"] == "6.85"
        assert result["as_of_date"] == "2026-07-02"

    def test_fbi_crime_requires_key(self):
        client = FbiCrimeClient(FbiCrimeSettings(enabled=True, api_key=None))
        result = client.state_crime_summary("CA")
        assert "FBI_CRIME_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_fbi_crime_parses_results(self):
        def handler(request):
            assert request.url.params.get("api_key") == "fbikey"
            assert "cde" in str(request.url)
            # from/to are required MM-YYYY params supplied by the client.
            assert request.url.params.get("from")
            assert request.url.params.get("to")
            payload = {
                "offenses": {
                    "actuals": {
                        "California Offenses": {"01-2020": 14025, "02-2020": 13257}
                    },
                    "rates": {
                        "California Offenses": {"01-2020": 35.63, "02-2020": 33.68}
                    },
                }
            }
            return httpx.Response(200, json=payload)

        client = FbiCrimeClient(
            FbiCrimeSettings(enabled=True, api_key="fbikey"),
            http_client=_mock_client(handler),
        )
        result = client.state_crime_summary("CA")
        assert result["enabled"] is True
        assert result["result_count"] == 4
        assert any(
            r["metric"] == "actuals" and r["period"] == "01-2020"
            for r in result["results"]
        )

    def test_epa_parses_results(self):
        def handler(request):
            assert "efservice" in str(request.url)
            return httpx.Response(200, json=[{"facility_name": "Acme Plant"}])

        client = EpaClient(EpaSettings(enabled=True), http_client=_mock_client(handler))
        result = client.environmental_hazards_by_state("CA")
        assert result["enabled"] is True
        assert result["results"][0]["facility_name"] == "Acme Plant"

    def test_noaa_two_step_lookup(self):
        def handler(request):
            if "/points/" in str(request.url):
                assert request.headers.get("User-Agent")
                # NWS 4-decimal-place requirement: a raw, full-precision
                # coordinate must be rounded before it reaches the URL.
                assert "/points/33.9827,-117.3731" in str(request.url)
                return httpx.Response(
                    200,
                    json={
                        "properties": {
                            "forecast": "https://api.weather.gov/gridpoints/LWX/96,70/forecast"
                        }
                    },
                )
            return httpx.Response(
                200,
                json={
                    "properties": {"periods": [{"name": "Today", "temperature": 75}]}
                },
            )

        client = NoaaClient(
            NoaaSettings(enabled=True), http_client=_mock_client(handler)
        )
        result = client.forecast(33.982735, -117.373137)
        assert result["enabled"] is True
        assert result["result_count"] == 1
        assert result["results"][0]["name"] == "Today"

    def test_zillow_requires_key(self):
        client = ZillowClient(ZillowSettings(enabled=True, api_key=None))
        result = client.lookup_zestimate("1 Main St")
        assert "ZILLOW_API_KEY" in result["missing_settings"]
        assert result["results"] == []

    def test_zillow_parses_results(self):
        def handler(request):
            assert request.url.params.get("access_token") == "zkey"
            assert request.headers.get("Authorization") == "Bearer zkey"
            assert "/zestimates" in str(request.url)
            return httpx.Response(
                200, json={"bundle": [{"zpid": "12345", "zestimate": 600000}]}
            )

        client = ZillowClient(
            ZillowSettings(enabled=True, api_key="zkey"),
            http_client=_mock_client(handler),
        )
        result = client.lookup_zestimate("1 Main St")
        assert result["enabled"] is True
        assert result["results"][0]["zpid"] == "12345"


class TestIntegrationTools:
    async def test_integration_status_tool(self, mcp_server):
        result = await call_tool_json(mcp_server, "integration_status", {})
        assert "census" in result
        assert "rentcast" in result
        assert "walkscore" in result
        assert "fema" in result
        assert "fred" in result
        assert "fbi_crime" in result
        assert "epa" in result
        assert "noaa" in result
        assert "zillow" in result

    async def test_lookup_live_property_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("RENTCAST_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "lookup_live_property", {"address": "1 Main St"}
        )
        assert result["enabled"] is False

    async def test_lookup_live_zestimate_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("ZILLOW_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "lookup_live_zestimate", {"address": "1 Main St"}
        )
        assert result["enabled"] is False

    async def test_get_live_demographics_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("CENSUS_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_demographics", {"state_fips": "06"}
        )
        assert result["enabled"] is False

    async def test_get_live_walk_score_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("WALKSCORE_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server,
            "get_live_walk_score",
            {"address": "1 Main St", "lat": 47.6, "lon": -122.3},
        )
        assert result["enabled"] is False

    async def test_get_live_flood_zone_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("FEMA_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_flood_zone", {"lat": 32.3, "lon": -96.6}
        )
        assert result["enabled"] is False

    async def test_get_live_mortgage_rate_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("FRED_ENABLED", raising=False)
        result = await call_tool_json(mcp_server, "get_live_mortgage_rate", {})
        assert result["enabled"] is False

    async def test_get_live_crime_summary_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("FBI_CRIME_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_crime_summary", {"state_abbr": "CA"}
        )
        assert result["enabled"] is False

    async def test_get_live_environmental_hazards_disabled(
        self, mcp_server, monkeypatch
    ):
        monkeypatch.delenv("EPA_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_environmental_hazards", {"state_abbr": "CA"}
        )
        assert result["enabled"] is False

    async def test_get_live_weather_forecast_disabled(self, mcp_server, monkeypatch):
        monkeypatch.delenv("NOAA_ENABLED", raising=False)
        result = await call_tool_json(
            mcp_server, "get_live_weather_forecast", {"lat": 38.9, "lon": -77.0}
        )
        assert result["enabled"] is False
