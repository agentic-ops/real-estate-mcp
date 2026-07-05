"""Zillow property-data adapter.

Zillow retired its public self-serve API in 2021. Live access to Zillow
Group data (Zestimates, public records, Zillow economic research) now
requires an approved enterprise license via Bridge Interactive
(https://www.bridgeinteractive.com/developers/zillow-group-data/) or an
equivalent licensed data provider -- typically an enterprise agreement
starting around $500/month, not a self-serve signup. This adapter is
therefore treated like RentCast: metered/paid and off by default, with a
configurable ``base_url`` so it can point at whichever provider issued
your access token.

Auth: an ``access_token`` query parameter (Bridge Interactive convention)
carrying your provider-issued token.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import ZillowSettings, get_integration_settings
from utils import audit


class ZillowClient:
    """Thin, testable wrapper over a Zillow Group data API (e.g. Bridge)."""

    def __init__(
        self,
        settings: Optional[ZillowSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().zillow
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the token)."""

        return {
            "source": "zillow",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": (
                "paid/enterprise; requires an approved Zillow Group data "
                "license (e.g. Bridge Interactive, ~$500+/mo) -- there is "
                "no public self-serve Zillow API"
            ),
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def lookup_zestimate(self, address: str) -> Dict[str, Any]:
        """Look up a Zestimate-style valuation for an address."""

        audit(
            "zillow_lookup_zestimate",
            address=address,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "Zillow integration is disabled. Set ZILLOW_ENABLED=true "
                    "to enable it (requires an approved data license)."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "Zillow is enabled but no API key/token is set. Set "
                    "ZILLOW_API_KEY."
                ),
                "results": [],
            }

        params = {"address": address, "access_token": self.settings.api_key}
        try:
            client = self._get_client()
            response = client.get(self.settings.base_url, params=params)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "address": address,
                "error": f"Zillow request failed: {exc}",
                "results": [],
            }

        results = payload if isinstance(payload, list) else payload.get("bundle", [])
        return {
            "source": "zillow",
            "enabled": True,
            "address": address,
            "result_count": len(results),
            "results": results,
        }
