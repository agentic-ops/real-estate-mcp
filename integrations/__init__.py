"""Optional live real-estate-data integrations.

This package holds adapters for external data providers that are *disabled
by default* and enabled per-integration via feature flags and API
credentials (see :mod:`integrations.config`).

* :mod:`integrations.census` -- U.S. Census Bureau API (free, preferred for
  demographic context).
* :mod:`integrations.rentcast` -- RentCast property data (metered; may incur
  costs). Off by default.
"""

from __future__ import annotations

from integrations.census import CensusClient
from integrations.config import (
    CensusSettings,
    IntegrationSettings,
    RentCastSettings,
    get_integration_settings,
)
from integrations.rentcast import RentCastClient

__all__ = [
    "CensusSettings",
    "RentCastSettings",
    "IntegrationSettings",
    "get_integration_settings",
    "CensusClient",
    "RentCastClient",
]
