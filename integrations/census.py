"""U.S. Census Bureau API adapter (American Community Survey).

The Census API is free, but as of Census's own developer docs and
confirmed live (2026-07-05), every query now requires an API key --
keyless requests 302-redirect to ``missing_key.html``. This historically
optional-key framing is outdated; request a free key at
https://api.census.gov/data/key_signup.html. Disabled by default; when
disabled or unconfigured it returns a structured status payload instead of
making any network call.

API reference: https://www.census.gov/data/developers/data-sets.html
Verified live (2026-07-05): GET .../2022/acs/acs5?get=...&for=state:06
  (no key)          -> HTTP 302 to missing_key.html
  (key=<bogus>)     -> HTTP 302 to invalid_key.html
  (key=<valid>)     -> HTTP 200 with the documented [[header...], [row...]]
                       array shape (per Census's official example calls).
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import CensusSettings, get_integration_settings
from utils import audit


class CensusClient:
    """Thin, testable wrapper over the Census Bureau REST API."""

    def __init__(
        self,
        settings: Optional[CensusSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().census
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (never leaks the key)."""

        return {
            "source": "census",
            "enabled": self.settings.enabled,
            "configured": self.settings.configured,
            "base_url": self.settings.base_url,
            "has_api_key": bool(self.settings.api_key),
            "missing_settings": self.settings.missing_settings(),
            "cost": (
                "free, but Census now requires an API key for every "
                "request; preferred demographic source"
            ),
        }

    def _get_client(self):
        if self._http_client is not None:
            return self._http_client
        import httpx

        return httpx.Client(timeout=30.0)

    def demographics(
        self,
        state_fips: str,
        year: int = 2022,
        dataset: str = "acs/acs5",
    ) -> Dict[str, Any]:
        """Fetch basic ACS demographics for a state FIPS code."""

        audit(
            "census_demographics",
            state_fips=state_fips,
            year=year,
            enabled=self.settings.enabled,
        )
        if not self.settings.enabled:
            return {
                **self.status(),
                "state_fips": state_fips,
                "message": (
                    "Census integration is disabled. Set CENSUS_ENABLED=true "
                    "to enable it."
                ),
                "results": [],
            }
        if not self.settings.configured:
            return {
                **self.status(),
                "state_fips": state_fips,
                "message": (
                    "Census is enabled but no API key is set. Census now "
                    "requires a key for every request -- get a free one at "
                    "https://api.census.gov/data/key_signup.html and set "
                    "CENSUS_API_KEY."
                ),
                "results": [],
            }

        # B01003_001E = total population; B19013_001E = median household income.
        params = {
            "get": "NAME,B01003_001E,B19013_001E",
            "for": f"state:{state_fips}",
            "key": self.settings.api_key,
        }
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/{year}/{dataset}",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "state_fips": state_fips,
                "error": f"Census request failed: {exc}",
                "results": [],
            }

        rows = []
        if isinstance(payload, list) and len(payload) > 1:
            header = payload[0]
            for record in payload[1:]:
                rows.append(dict(zip(header, record)))
        return {
            "source": "census",
            "enabled": True,
            "state_fips": state_fips,
            "year": year,
            "dataset": dataset,
            "result_count": len(rows),
            "results": rows,
        }
