"""Optional live real-estate-data integrations.

This package holds adapters for external data providers that are *disabled
by default* and enabled per-integration via feature flags and API
credentials (see :mod:`integrations.config`).

Free / keyless-or-free-key sources:

* :mod:`integrations.census` -- U.S. Census Bureau API (demographics).
* :mod:`integrations.walkscore` -- Walk/Transit/Bike Score (free tier).
* :mod:`integrations.fema` -- FEMA National Flood Hazard Layer (flood zones).
* :mod:`integrations.fred` -- FRED economic data (mortgage rates, etc.).
* :mod:`integrations.fbi_crime` -- FBI Crime Data API (crime statistics).
* :mod:`integrations.epa` -- EPA Envirofacts (environmental hazards).
* :mod:`integrations.noaa` -- National Weather Service (forecasts).

Paid / metered sources:

* :mod:`integrations.rentcast` -- RentCast property data (metered).
* :mod:`integrations.zillow` -- Zillow Group data (enterprise-licensed).
"""

from __future__ import annotations

from integrations.census import CensusClient
from integrations.config import (
    CensusSettings,
    EpaSettings,
    FbiCrimeSettings,
    FemaSettings,
    FredSettings,
    IntegrationSettings,
    NoaaSettings,
    RentCastSettings,
    WalkScoreSettings,
    ZillowSettings,
    get_integration_settings,
)
from integrations.epa import EpaClient
from integrations.fbi_crime import FbiCrimeClient
from integrations.fema import FemaClient
from integrations.fred import FredClient
from integrations.noaa import NoaaClient
from integrations.rentcast import RentCastClient
from integrations.walkscore import WalkScoreClient
from integrations.zillow import ZillowClient

__all__ = [
    "CensusSettings",
    "RentCastSettings",
    "WalkScoreSettings",
    "FemaSettings",
    "FredSettings",
    "FbiCrimeSettings",
    "EpaSettings",
    "NoaaSettings",
    "ZillowSettings",
    "IntegrationSettings",
    "get_integration_settings",
    "CensusClient",
    "RentCastClient",
    "WalkScoreClient",
    "FemaClient",
    "FredClient",
    "FbiCrimeClient",
    "EpaClient",
    "NoaaClient",
    "ZillowClient",
]
