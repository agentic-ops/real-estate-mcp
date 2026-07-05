"""National Weather Service (api.weather.gov) adapter.

Free and keyless. NWS asks every client to identify itself with a
descriptive ``User-Agent`` header instead of an API key. Fetching a
forecast is a two-step lookup: resolve the ``lat,lon`` to a forecast grid
via ``/points``, then fetch the forecast URL returned in that response.
Disabled by default; when disabled it returns a structured status payload
instead of making any network call.

API reference: https://www.weather.gov/documentation/services-web-api

IMPORTANT (verified live 2026-07-05): ``/points/{lat},{lon}`` requires
coordinates rounded to 4 decimal places -- higher precision (e.g. a raw
GPS reading) gets a **301 redirect** to the rounded form. ``httpx.Client``
does not follow redirects by default, so an unrounded coordinate would
otherwise fail with a confusing "Redirect response" error. This adapter
rounds to 4 decimals before requesting.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import NoaaSettings, get_integration_settings
from utils import audit


class NoaaClient:
    """Thin, testable wrapper over the National Weather Service REST API."""

    def __init__(
        self,
        settings: Optional[NoaaSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().noaa
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (no key to leak)."""

        return {
            "source": "noaa",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "free (federal, keyless; identifies itself via User-Agent)",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch the multi-day forecast for a coordinate."""

        audit("noaa_forecast", lat=lat, lon=lon, enabled=self.settings.enabled)
        if not self.settings.enabled:
            return {
                **self.status(),
                "lat": lat,
                "lon": lon,
                "message": (
                    "NOAA integration is disabled. Set NOAA_ENABLED=true to "
                    "enable it."
                ),
                "results": [],
            }

        headers = {"User-Agent": self.settings.contact}
        # NWS requires <= 4 decimal places on /points; anything more precise
        # 301-redirects to the rounded form, which httpx won't follow by
        # default.
        rounded_lat, rounded_lon = round(lat, 4), round(lon, 4)
        try:
            client = self._get_client()
            points_response = client.get(
                f"{self.settings.base_url}/points/{rounded_lat},{rounded_lon}",
                headers=headers,
            )
            points_response.raise_for_status()
            points_payload = points_response.json()
            forecast_url = points_payload.get("properties", {}).get("forecast")
            if not forecast_url:
                raise ValueError("no forecast URL returned for this location")
            forecast_response = client.get(forecast_url, headers=headers)
            forecast_response.raise_for_status()
            forecast_payload = forecast_response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "lat": lat,
                "lon": lon,
                "error": f"NOAA request failed: {exc}",
                "results": [],
            }

        periods = forecast_payload.get("properties", {}).get("periods", [])
        return {
            "source": "noaa",
            "enabled": True,
            "lat": lat,
            "lon": lon,
            "result_count": len(periods),
            "results": periods,
        }
