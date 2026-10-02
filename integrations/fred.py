"""FRED (Federal Reserve Economic Data) API adapter.

Free source, maintained by the St. Louis Fed, for economic time series --
including the weekly Freddie Mac Primary Mortgage Market Survey 30-year
fixed rate (series ``MORTGAGE30US``). A free API key is required. Disabled
by default; when disabled or unconfigured it returns a structured status
payload instead of making any network call.

API reference: https://fred.stlouisfed.org/docs/api/fred/
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import FredSettings, get_integration_settings, redact_secret
from utils import audit

MORTGAGE_30YR_SERIES_ID = "MORTGAGE30US"


class FredClient:
    """Thin, testable wrapper over the FRED REST API."""

    def __init__(
        self,
        settings: Optional[FredSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().fred
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the key)."""

        return {
            "source": "fred",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "free (requires a free API key)",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def series_observations(
        self, series_id: str = MORTGAGE_30YR_SERIES_ID, limit: int = 1
    ) -> Dict[str, Any]:
        """Fetch the most recent observation(s) for a FRED series."""

        audit(
            "fred_series_observations",
            series_id=series_id,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "series_id": series_id,
                "message": (
                    "FRED integration is disabled. Set FRED_ENABLED=true to "
                    "enable it."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "series_id": series_id,
                "message": ("FRED is enabled but no API key is set. Set FRED_API_KEY."),
                "results": [],
            }

        params = {
            "series_id": series_id,
            "api_key": self.settings.api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        }
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/series/observations", params=params
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "series_id": series_id,
                "error": "FRED request failed: "
                + redact_secret(exc, self.settings.api_key),
                "results": [],
            }

        results = payload.get("observations", [])
        return {
            "source": "fred",
            "enabled": True,
            "series_id": series_id,
            "result_count": len(results),
            "results": results,
        }

    def current_mortgage_rate_30yr(self) -> Dict[str, Any]:
        """Convenience wrapper for the latest 30-year fixed mortgage rate."""

        result = self.series_observations(MORTGAGE_30YR_SERIES_ID, limit=1)
        if result.get("results"):
            latest = result["results"][0]
            result["latest_rate_percent"] = latest.get("value")
            result["as_of_date"] = latest.get("date")
        return result
