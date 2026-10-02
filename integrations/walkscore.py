"""Walk Score API adapter (Walk Score, Transit Score, Bike Score).

Walk Score's consumer-facing API tier is free for up to 5,000 calls/day,
but still requires a free API key (request one at
https://www.walkscore.com/professional/api.php). Disabled by default; when
disabled or unconfigured it returns a structured status payload instead of
making any network call.

API reference: https://www.walkscore.com/professional/api.php

IMPORTANT (verified live 2026-07-05): Walk Score returns HTTP 200 even for
key/quota/IP errors -- the actual outcome is only visible in the JSON body's
``status`` field (e.g. an invalid key returns ``HTTP 200 {"status": 40}``).
``response.raise_for_status()`` alone will NOT catch this, so this adapter
explicitly inspects ``status`` and surfaces the documented error text
instead of reporting a false success.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import (
    WalkScoreSettings,
    get_integration_settings,
    redact_secret,
)
from utils import audit

# https://www.walkscore.com/professional/api.php -- "Status and Error Codes"
STATUS_MESSAGES = {
    1: "Walk Score successfully returned.",
    2: "Score is being calculated and is not currently available.",
    30: "Invalid latitude/longitude.",
    31: "Walk Score API internal error.",
    40: "Your WSAPIKEY is invalid.",
    41: "Your daily API quota has been exceeded.",
    42: "Your IP address has been blocked.",
}
SUCCESS_STATUS_CODES = {1, 2}


class WalkScoreClient:
    """Thin, testable wrapper over the Walk Score REST API."""

    def __init__(
        self,
        settings: Optional[WalkScoreSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().walkscore
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the key)."""

        return {
            "source": "walkscore",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "free up to 5,000 calls/day for consumer-facing use",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def walk_score(
        self,
        address: str,
        lat: float,
        lon: float,
        include_transit: bool = True,
        include_bike: bool = True,
    ) -> Dict[str, Any]:
        """Fetch Walk/Transit/Bike Score for an address + coordinate pair."""

        audit(
            "walkscore_walk_score",
            address=address,
            lat=lat,
            lon=lon,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "Walk Score integration is disabled. Set "
                    "WALKSCORE_ENABLED=true to enable it."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "address": address,
                "message": (
                    "Walk Score is enabled but no API key is set. Set "
                    "WALKSCORE_API_KEY."
                ),
                "results": [],
            }

        params = {
            "address": address,
            "lat": lat,
            "lon": lon,
            "wsapikey": self.settings.api_key,
            "format": "json",
        }
        if include_transit:
            params["transit"] = 1
        if include_bike:
            params["bike"] = 1
        try:
            client = self._get_client()
            response = client.get(f"{self.settings.base_url}/score", params=params)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "address": address,
                "error": "Walk Score request failed: "
                + redact_secret(exc, self.settings.api_key),
                "results": [],
            }

        status_code: int = (
            payload.get("status", -1) if isinstance(payload, dict) else -1
        )
        if status_code not in SUCCESS_STATUS_CODES:
            message = STATUS_MESSAGES.get(status_code, "unknown error")
            return {
                **self.status(),
                "address": address,
                "error": f"Walk Score returned status {status_code}: {message}",
                "results": [],
            }

        return {
            "source": "walkscore",
            "enabled": True,
            "address": address,
            "pending": status_code == 2,
            "result_count": 1,
            "results": [payload],
        }
