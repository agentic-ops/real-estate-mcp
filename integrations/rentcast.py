"""RentCast property-data API adapter.

RentCast exposes property records, value estimates, and rent estimates via a
metered REST API. Requests draw against a monthly quota and may incur costs,
so this integration is off by default and requires an API key.

API reference: https://developers.rentcast.io/
Auth: an ``X-Api-Key: <key>`` header on every request.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import (
    RentCastSettings,
    get_integration_settings,
    redact_secret,
)
from utils import audit


class RentCastClient:
    """Thin, testable wrapper over the RentCast REST API."""

    def __init__(
        self,
        settings: Optional[RentCastSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().rentcast
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the key)."""

        return {
            "source": "rentcast",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "metered (monthly quota; may incur costs)",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def lookup_property(self, address: str, limit: int = 5) -> Dict[str, Any]:
        """Look up property records for an address; JSON-friendly dict."""

        audit(
            "rentcast_lookup_property",
            address=address,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "RentCast integration is disabled. Set RENTCAST_ENABLED=true "
                    "to enable it."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "RentCast is enabled but no API key is set. Set "
                    "RENTCAST_API_KEY."
                ),
                "results": [],
            }

        headers = {"X-Api-Key": self.settings.api_key}
        params = {"address": address, "limit": limit}
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/properties",
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "address": address,
                "error": "RentCast request failed: "
                + redact_secret(exc, self.settings.api_key),
                "results": [],
            }

        results = payload if isinstance(payload, list) else payload.get("results", [])
        return {
            "source": "rentcast",
            "enabled": True,
            "address": address,
            "result_count": len(results),
            "results": results[:limit],
        }
