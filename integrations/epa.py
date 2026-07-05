"""EPA Envirofacts API adapter.

A free, keyless REST service exposing EPA data holdings. This adapter
queries the Toxics Release Inventory (TRI) facility table as a proxy for
environmental-hazard due-diligence near a property or area. Disabled by
default; when disabled it returns a structured status payload instead of
making any network call.

API reference: https://www.epa.gov/enviro/envirofacts-data-service-api
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import EpaSettings, get_integration_settings
from utils import audit


class EpaClient:
    """Thin, testable wrapper over the EPA Envirofacts REST service."""

    def __init__(
        self,
        settings: Optional[EpaSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().epa
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (no key to leak)."""

        return {
            "source": "epa",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "free (federal, keyless)",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def environmental_hazards_by_state(
        self, state_abbr: str, limit: int = 25
    ) -> Dict[str, Any]:
        """List TRI-reporting facilities (potential environmental hazards)
        for a state, as a keyless due-diligence proxy."""

        audit(
            "epa_environmental_hazards",
            state_abbr=state_abbr,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "state_abbr": state_abbr,
                "message": (
                    "EPA integration is disabled. Set EPA_ENABLED=true to " "enable it."
                ),
                "results": [],
            }

        url = (
            f"{self.settings.base_url}/tri_facility/state_abbr/"
            f"{state_abbr}/rows/0:{max(limit - 1, 0)}/JSON"
        )
        try:
            client = self._get_client()
            response = client.get(url)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "state_abbr": state_abbr,
                "error": f"EPA request failed: {exc}",
                "results": [],
            }

        results = payload if isinstance(payload, list) else []
        return {
            "source": "epa",
            "enabled": True,
            "state_abbr": state_abbr,
            "result_count": len(results),
            "results": results[:limit],
        }
