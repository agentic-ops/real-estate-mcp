"""FBI Crime Data API adapter (Uniform Crime Reporting / NIBRS).

Free federal crime statistics, served today via the FBI Crime Data Explorer
(CDE) "summarized" endpoint. Requires a free api.data.gov key
(https://api.data.gov/signup/). Disabled by default; when disabled or
unconfigured it returns a structured status payload instead of making any
network call.

API reference: https://cde.ucr.cjis.gov/ (Swagger: https://crime-data-explorer.fr.cloud.gov/api)

Verified live endpoint (2026-07-05):
  GET https://api.usa.gov/crime/fbi/cde/summarized/state/{state_abbr}/{offense}
      ?api_key=...&from=MM-YYYY&to=MM-YYYY
The legacy ``.../sapi/api/summarized/...`` path (still referenced in older
tutorials and the FBI's own developer portal copy) now 404s -- the live
service is under ``.../cde/summarized/...``. The ``from``/``to`` query
params are REQUIRED and must be ``MM-YYYY``; omitting them returns a 400.
The response is NOT a flat "results" list -- it nests monthly figures under
``offenses.actuals`` and ``offenses.rates``, each keyed by a human-readable
category label (e.g. ``"California Offenses"``) mapping to a
``{"MM-YYYY": value}`` dict. This adapter flattens that into a tabular
``results`` list of ``{metric, category, period, value}`` records.
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from integrations.config import FbiCrimeSettings, get_integration_settings
from utils import audit


def _default_date_range(months: int = 12) -> tuple[str, str]:
    """Return a sane (from, to) MM-YYYY range ending last full month."""

    today = datetime.date.today().replace(day=1)
    end = today - datetime.timedelta(days=1)  # last day of previous month
    year, month = end.year, end.month
    for _ in range(months - 1):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return f"{month:02d}-{year}", f"{end.month:02d}-{end.year}"


def _flatten_offenses(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten the nested ``offenses.{actuals,rates}`` structure."""

    records: List[Dict[str, Any]] = []
    offenses = payload.get("offenses", {}) if isinstance(payload, dict) else {}
    for metric in ("actuals", "rates"):
        for category, by_period in (offenses.get(metric) or {}).items():
            if not isinstance(by_period, dict):
                continue
            for period, value in by_period.items():
                records.append(
                    {
                        "metric": metric,
                        "category": category,
                        "period": period,
                        "value": value,
                    }
                )
    return records


class FbiCrimeClient:
    """Thin, testable wrapper over the FBI Crime Data (CDE) REST API."""

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
        self,
        state_abbr: str,
        offense: str = "violent-crime",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch summarized state-level crime counts for an offense type.

        ``from_date``/``to_date`` must be ``MM-YYYY`` strings (required by
        the live API); when omitted, defaults to the trailing 12 full
        months.
        """

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

        default_from, default_to = _default_date_range()
        from_date = from_date or default_from
        to_date = to_date or default_to
        params = {
            "api_key": self.settings.api_key,
            "from": from_date,
            "to": to_date,
        }
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/summarized/state/" f"{state_abbr}/{offense}",
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

        results = _flatten_offenses(payload)
        return {
            "source": "fbi_crime",
            "enabled": True,
            "state_abbr": state_abbr,
            "offense": offense,
            "from": from_date,
            "to": to_date,
            "result_count": len(results),
            "results": results,
        }
