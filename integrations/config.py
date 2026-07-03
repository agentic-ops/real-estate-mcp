"""Configuration for optional live real-estate-data integrations.

Every integration is controlled by two things:

1. A **feature flag** (an environment variable such as ``RENTCAST_ENABLED``)
   that turns the integration on or off. All integrations default to
   **off** so that a fresh fork never makes surprise network calls or
   incurs API costs.
2. **API credentials / keys** supplied via environment variables.

Settings are read from the environment on demand so that a running server
(or a test) can re-read them after changing an environment variable.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

CENSUS_DEFAULT_BASE_URL = "https://api.census.gov/data"
RENTCAST_DEFAULT_BASE_URL = "https://api.rentcast.io/v1"


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _opt_env(name: str) -> Optional[str]:
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


@dataclass
class CensusSettings:
    """U.S. Census Bureau API feature flag + optional key.

    The Census API is free. An API key is optional (it raises rate limits)
    so this integration is considered "configured" even without one. It is
    still off by default so forks opt in explicitly.
    """

    enabled: bool = False
    base_url: str = CENSUS_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "CensusSettings":
        return cls(
            enabled=_bool_env("CENSUS_ENABLED", False),
            base_url=os.environ.get("CENSUS_BASE_URL", CENSUS_DEFAULT_BASE_URL).rstrip(
                "/"
            ),
            api_key=_opt_env("CENSUS_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        # The Census API works without a key (rate-limited).
        return True

    def missing_settings(self) -> List[str]:
        return []


@dataclass
class RentCastSettings:
    """RentCast property-data API feature flag + credentials.

    RentCast is a *metered* service: requests draw against a monthly quota
    and may incur costs. It is off by default and requires an API key.
    """

    enabled: bool = False
    base_url: str = RENTCAST_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "RentCastSettings":
        return cls(
            enabled=_bool_env("RENTCAST_ENABLED", False),
            base_url=os.environ.get(
                "RENTCAST_BASE_URL", RENTCAST_DEFAULT_BASE_URL
            ).rstrip("/"),
            api_key=_opt_env("RENTCAST_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def missing_settings(self) -> List[str]:
        return [] if self.api_key else ["RENTCAST_API_KEY"]


@dataclass
class IntegrationSettings:
    """Aggregate settings for all optional integrations."""

    census: CensusSettings
    rentcast: RentCastSettings

    @classmethod
    def from_env(cls) -> "IntegrationSettings":
        return cls(
            census=CensusSettings.from_env(),
            rentcast=RentCastSettings.from_env(),
        )


def get_integration_settings() -> IntegrationSettings:
    """Read the current integration settings from the environment."""

    return IntegrationSettings.from_env()
