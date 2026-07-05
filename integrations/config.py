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
WALKSCORE_DEFAULT_BASE_URL = "https://api.walkscore.com"
FEMA_DEFAULT_BASE_URL = (
    "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer"
)
FRED_DEFAULT_BASE_URL = "https://api.stlouisfed.org/fred"
# The legacy "sapi" host (api.usa.gov/crime/fbi/sapi) now 404s; the FBI Crime
# Data Explorer serves the same "summarized" endpoint under "cde".
FBI_CRIME_DEFAULT_BASE_URL = "https://api.usa.gov/crime/fbi/cde"
EPA_DEFAULT_BASE_URL = "https://data.epa.gov/efservice"
NOAA_DEFAULT_BASE_URL = "https://api.weather.gov"
NOAA_DEFAULT_CONTACT = "real-estate-mcp (no-contact-configured@example.com)"
ZILLOW_DEFAULT_BASE_URL = "https://api.bridgedataoutput.com/api/v2/zestimates_v2"


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
class WalkScoreSettings:
    """Walk Score API feature flag + credentials.

    Walk Score, Transit Score, and Bike Score are free for consumer-facing
    use up to 5,000 calls/day, but still require a free API key. Off by
    default; requires ``WALKSCORE_API_KEY`` once enabled.
    """

    enabled: bool = False
    base_url: str = WALKSCORE_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "WalkScoreSettings":
        return cls(
            enabled=_bool_env("WALKSCORE_ENABLED", False),
            base_url=os.environ.get(
                "WALKSCORE_BASE_URL", WALKSCORE_DEFAULT_BASE_URL
            ).rstrip("/"),
            api_key=_opt_env("WALKSCORE_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def missing_settings(self) -> List[str]:
        return [] if self.api_key else ["WALKSCORE_API_KEY"]


@dataclass
class FemaSettings:
    """FEMA National Flood Hazard Layer (NFHL) feature flag.

    A free, federal, keyless ArcGIS REST service used to look up flood
    zones by coordinate. Off by default like every other integration.
    """

    enabled: bool = False
    base_url: str = FEMA_DEFAULT_BASE_URL

    @classmethod
    def from_env(cls) -> "FemaSettings":
        return cls(
            enabled=_bool_env("FEMA_ENABLED", False),
            base_url=os.environ.get("FEMA_BASE_URL", FEMA_DEFAULT_BASE_URL).rstrip("/"),
        )

    @property
    def configured(self) -> bool:
        # No key required.
        return True

    def missing_settings(self) -> List[str]:
        return []


@dataclass
class FredSettings:
    """FRED (Federal Reserve Economic Data) API feature flag + credentials.

    Free source for the weekly Freddie Mac Primary Mortgage Market Survey
    (series ``MORTGAGE30US``) and other economic indicators. Requires a
    free API key from https://fredaccount.stlouisfed.org/apikeys.
    """

    enabled: bool = False
    base_url: str = FRED_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "FredSettings":
        return cls(
            enabled=_bool_env("FRED_ENABLED", False),
            base_url=os.environ.get("FRED_BASE_URL", FRED_DEFAULT_BASE_URL).rstrip("/"),
            api_key=_opt_env("FRED_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def missing_settings(self) -> List[str]:
        return [] if self.api_key else ["FRED_API_KEY"]


@dataclass
class FbiCrimeSettings:
    """FBI Crime Data API (UCR/NIBRS) feature flag + credentials.

    Free federal crime statistics. Requires a free api.data.gov key from
    https://api.data.gov/signup/.
    """

    enabled: bool = False
    base_url: str = FBI_CRIME_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "FbiCrimeSettings":
        return cls(
            enabled=_bool_env("FBI_CRIME_ENABLED", False),
            base_url=os.environ.get(
                "FBI_CRIME_BASE_URL", FBI_CRIME_DEFAULT_BASE_URL
            ).rstrip("/"),
            api_key=_opt_env("FBI_CRIME_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def missing_settings(self) -> List[str]:
        return [] if self.api_key else ["FBI_CRIME_API_KEY"]


@dataclass
class EpaSettings:
    """EPA Envirofacts API feature flag.

    A free, keyless REST service exposing EPA data holdings (Toxics
    Release Inventory, Superfund, RCRAInfo, etc.) used here as an
    environmental-hazard proxy for area due-diligence.
    """

    enabled: bool = False
    base_url: str = EPA_DEFAULT_BASE_URL

    @classmethod
    def from_env(cls) -> "EpaSettings":
        return cls(
            enabled=_bool_env("EPA_ENABLED", False),
            base_url=os.environ.get("EPA_BASE_URL", EPA_DEFAULT_BASE_URL).rstrip("/"),
        )

    @property
    def configured(self) -> bool:
        return True

    def missing_settings(self) -> List[str]:
        return []


@dataclass
class NoaaSettings:
    """National Weather Service (api.weather.gov) feature flag.

    Free and keyless, but NWS asks every client to identify itself with a
    descriptive ``User-Agent`` header (app name + contact email) instead
    of an API key.
    """

    enabled: bool = False
    base_url: str = NOAA_DEFAULT_BASE_URL
    contact: str = NOAA_DEFAULT_CONTACT

    @classmethod
    def from_env(cls) -> "NoaaSettings":
        return cls(
            enabled=_bool_env("NOAA_ENABLED", False),
            base_url=os.environ.get("NOAA_BASE_URL", NOAA_DEFAULT_BASE_URL).rstrip("/"),
            contact=os.environ.get("NOAA_CONTACT", NOAA_DEFAULT_CONTACT),
        )

    @property
    def configured(self) -> bool:
        # No key required; a default contact string is always present.
        return True

    def missing_settings(self) -> List[str]:
        return []


@dataclass
class ZillowSettings:
    """Zillow property-data feature flag + credentials.

    Zillow retired its public self-serve API in 2021. Live access now
    requires an approved Zillow Group Data license via Bridge Interactive
    (https://www.bridgeinteractive.com/developers/zillow-group-data/) --
    an enterprise agreement typically starting around $500/month -- or an
    equivalent licensed provider. This adapter is metered/paid and off by
    default, just like RentCast, and requires an API/access token plus a
    base URL matching whatever provider issued that token.
    """

    enabled: bool = False
    base_url: str = ZILLOW_DEFAULT_BASE_URL
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "ZillowSettings":
        return cls(
            enabled=_bool_env("ZILLOW_ENABLED", False),
            base_url=os.environ.get("ZILLOW_BASE_URL", ZILLOW_DEFAULT_BASE_URL).rstrip(
                "/"
            ),
            api_key=_opt_env("ZILLOW_API_KEY"),
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def missing_settings(self) -> List[str]:
        return [] if self.api_key else ["ZILLOW_API_KEY"]


@dataclass
class IntegrationSettings:
    """Aggregate settings for all optional integrations."""

    census: CensusSettings
    rentcast: RentCastSettings
    walkscore: WalkScoreSettings
    fema: FemaSettings
    fred: FredSettings
    fbi_crime: FbiCrimeSettings
    epa: EpaSettings
    noaa: NoaaSettings
    zillow: ZillowSettings

    @classmethod
    def from_env(cls) -> "IntegrationSettings":
        return cls(
            census=CensusSettings.from_env(),
            rentcast=RentCastSettings.from_env(),
            walkscore=WalkScoreSettings.from_env(),
            fema=FemaSettings.from_env(),
            fred=FredSettings.from_env(),
            fbi_crime=FbiCrimeSettings.from_env(),
            epa=EpaSettings.from_env(),
            noaa=NoaaSettings.from_env(),
            zillow=ZillowSettings.from_env(),
        )


def get_integration_settings() -> IntegrationSettings:
    """Read the current integration settings from the environment."""

    return IntegrationSettings.from_env()
