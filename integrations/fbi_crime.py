"""FBI Crime Data API adapter (Uniform Crime Reporting / NIBRS).

Free federal crime statistics published by the FBI's Crime Data Explorer.
Requires a free api.data.gov key (https://api.data.gov/signup/). Disabled
by default; when disabled or unconfigured it returns a structured status
payload instead of making any network call.

API reference: https://crime-data-explorer.fr.cloud.gov/api
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import FbiCrimeSettings, get_integration_settings
from utils import audit


class FbiCrimeClient:
    """Thin, testable wrapper over the FBI Crime Data REST API."""

    def __init__(
        self,
        settings: Optional[FbiCrimeSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().fbi_crime
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the key)."""

        return {
            "source": "fbi_crime",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "missing_settings": self.settings.missing_settings(),
            "cost": "free (requires a free api.data.gov key)",
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def state_crime_summary(
        self, state_abbr: str, offense: str = "violent-crime"
    ) -> Dict[str, Any]:
        """Fetch summarized state-level crime counts for an offense type."""

        audit(
            "fbi_crime_state_summary",
            state_abbr=state_abbr,
            offense=offense,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "state_abbr": state_abbr,
                "offense": offense,
                "message": (
                    "FBI Crime Data integration is disabled. Set "
                    "FBI_CRIME_ENABLED=true to enable it."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "state_abbr": state_abbr,
                "offense": offense,
                "message": (
                    "FBI Crime Data is enabled but no API key is set. Set "
                    "FBI_CRIME_API_KEY."
                ),
                "results": [],
            }

        params = {"api_key": self.settings.api_key}
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/api/summarized/state/"
                f"{state_abbr}/{offense}",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "state_abbr": state_abbr,
                "offense": offense,
                "error": f"FBI Crime Data request failed: {exc}",
                "results": [],
            }

        results = payload.get("results", []) if isinstance(payload, dict) else []
        return {
            "source": "fbi_crime",
            "enabled": True,
            "state_abbr": state_abbr,
            "offense": offense,
            "result_count": len(results),
            "results": results,
        }
