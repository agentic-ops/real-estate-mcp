"""FEMA National Flood Hazard Layer (NFHL) adapter.

A free, federal, keyless ArcGIS REST service that returns the FEMA flood
zone(s) intersecting a coordinate -- useful for buyer due-diligence and
flood-insurance disclosure context. Disabled by default; when disabled it
returns a structured status payload instead of making any network call.

API reference: https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from integrations.config import FemaSettings, get_integration_settings
from utils import audit

# Layer 28 = "Flood Hazard Zones" polygons in the public NFHL MapServer.
FLOOD_HAZARD_ZONE_LAYER = 28


class FemaClient:
    """Thin, testable wrapper over the FEMA NFHL ArcGIS REST service."""

    def __init__(
        self,
        settings: Optional[FemaSettings] = None,
        http_client: Any = None,
    ) -> None:
        self.settings = settings or get_integration_settings().fema
        self._http_client = http_client

    @property
    def enabled(self) -> bool:
        return self.settings.enabled

    def status(self) -> Dict[str, Any]:
        """Return a non-sensitive status report (no key to leak)."""

        return {
            "source": "fema",
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

    def flood_zone(self, lat: float, lon: float) -> Dict[str, Any]:
        """Look up the FEMA flood hazard zone(s) at a coordinate."""

        audit("fema_flood_zone", lat=lat, lon=lon, enabled=self.settings.enabled)
        if not self.settings.enabled:
            return {
                **self.status(),
                "lat": lat,
                "lon": lon,
                "message": (
                    "FEMA integration is disabled. Set FEMA_ENABLED=true to "
                    "enable it."
                ),
                "results": [],
            }

        params = {
            "where": "1=1",
            "geometry": f"{lon},{lat}",
            "geometryType": "esriGeometryPoint",
            "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "FLD_ZONE,ZONE_SUBTY,SFHA_TF",
            "returnGeometry": "false",
            "f": "json",
        }
        try:
            client = self._get_client()
            response = client.get(
                f"{self.settings.base_url}/{FLOOD_HAZARD_ZONE_LAYER}/query",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            return {
                **self.status(),
                "lat": lat,
                "lon": lon,
                "error": f"FEMA request failed: {exc}",
                "results": [],
            }

        features = payload.get("features", [])
        results = [feature.get("attributes", {}) for feature in features]
        return {
            "source": "fema",
            "enabled": True,
            "lat": lat,
            "lon": lon,
            "result_count": len(results),
            "results": results,
        }
