# Integrations

Optional adapters for external real-estate data providers. **All integrations
are disabled by default** and enabled per-integration via environment
variables. When disabled or unconfigured, the adapters return a structured
status payload and make **no** network calls.

| Module | Enable flag | Credentials | Cost |
|--------|-------------|-------------|------|
| `census.py` | `CENSUS_ENABLED` | `CENSUS_API_KEY` (optional) | Free (rate-limited) |
| `walkscore.py` | `WALKSCORE_ENABLED` | `WALKSCORE_API_KEY` (required) | Free up to 5,000 calls/day |
| `fema.py` | `FEMA_ENABLED` | none | Free (federal, keyless) |
| `fred.py` | `FRED_ENABLED` | `FRED_API_KEY` (required) | Free |
| `fbi_crime.py` | `FBI_CRIME_ENABLED` | `FBI_CRIME_API_KEY` (required) | Free |
| `epa.py` | `EPA_ENABLED` | none | Free (federal, keyless) |
| `noaa.py` | `NOAA_ENABLED` | none (sets a `User-Agent`) | Free (federal, keyless) |
| `rentcast.py` | `RENTCAST_ENABLED` | `RENTCAST_API_KEY` (required) | Metered; may incur cost |
| `zillow.py` | `ZILLOW_ENABLED` | `ZILLOW_API_KEY` (required) | Paid/enterprise; requires an approved data license |

- `config.py` reads settings from the environment on demand (so a running
  server or a test can re-read after changing a variable).
- Each client exposes a `status()` method that reports enabled/configured
  state **without** ever returning the API key.
- The HTTP client is injectable (`http_client=`), which is how the test suite
  swaps in `httpx.MockTransport` to stay fully network-free.

## Enabling

```bash
# Free demographic context
export CENSUS_ENABLED=true
# export CENSUS_API_KEY=...        # optional; raises rate limits

# Free Walk/Transit/Bike Score (requires a free key)
export WALKSCORE_ENABLED=true
export WALKSCORE_API_KEY=...

# Free FEMA flood zone lookups (no key)
export FEMA_ENABLED=true

# Free FRED economic data / mortgage rates (requires a free key)
export FRED_ENABLED=true
export FRED_API_KEY=...

# Free FBI crime statistics (requires a free api.data.gov key)
export FBI_CRIME_ENABLED=true
export FBI_CRIME_API_KEY=...

# Free EPA environmental hazard data (no key)
export EPA_ENABLED=true

# Free NOAA/NWS weather forecasts (no key)
export NOAA_ENABLED=true

# Metered property data (understand the billing implications first)
export RENTCAST_ENABLED=true
export RENTCAST_API_KEY=...

# Paid/enterprise Zillow Group data (requires an approved data license,
# e.g. Bridge Interactive; there is no public self-serve Zillow API)
export ZILLOW_ENABLED=true
export ZILLOW_API_KEY=...
```

See `.env.example` for the full list.
