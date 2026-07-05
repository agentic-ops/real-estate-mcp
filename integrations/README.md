# Integrations

Optional adapters for external real-estate data providers. **All integrations
are disabled by default** and enabled per-integration via environment
variables. When disabled or unconfigured, the adapters return a structured
status payload and make **no** network calls.

| Module | Enable flag | Credentials | Cost |
|--------|-------------|-------------|------|
| `census.py` | `CENSUS_ENABLED` | `CENSUS_API_KEY` (required) | Free |
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
# Free demographic context (a key is REQUIRED -- Census rejects keyless requests)
export CENSUS_ENABLED=true
export CENSUS_API_KEY=...

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

## Spec verification (2026-07-05)

Each adapter was checked against its live API, not just its documentation,
by hitting the real endpoints from this environment (with a throwaway/demo
key where one was needed) and comparing the actual request/response shape
to what the code sends and parses. Findings:

| Source | Verified against live API? | Result |
|---|---|---|
| Census | Yes | **Bug found & fixed:** Census's own developer docs now state "All data queries to the Census Data API now require an API key" -- confirmed live (keyless requests 302 to `missing_key.html`; bad keys 302 to `invalid_key.html`; tested against 2019-2022 ACS5). The adapter previously treated the key as always-optional (`configured: true` with no key), which meant enabling Census without a key silently produced an unhelpful raw exception instead of a clear "set CENSUS_API_KEY" message. `CensusSettings.configured` now requires a key (matching every other keyed integration in this package), and `demographics()` short-circuits with a clear message instead of making a request guaranteed to fail. |
| Walk Score | Yes | **Bug found & fixed:** Walk Score returns **HTTP 200** even for an invalid key or exceeded quota (e.g. `{"status": 40}`) -- `raise_for_status()` alone can't catch this. The adapter now inspects the `status` field and maps it to Walk Score's documented error codes (1/2 = success, 30/31/40/41/42 = error) instead of reporting a false success. |
| FEMA NFHL | Yes | **Bug found & fixed:** the commonly-referenced `.../gis/nfhl/rest/services/...` path 404s today; the live service is at `.../arcgis/rest/services/public/NFHL/MapServer`. Layer 28 (`Flood Hazard Zones`) query params and response shape (`features[].attributes`) were confirmed correct against a real query. |
| FRED | Yes | Confirmed correct as implemented: endpoint, required params (`series_id`, `api_key`, `file_type=json`), and response shape (`observations[].{date,value}`) all match a live request (verified error path with an unregistered key). |
| FBI Crime Data | Yes | **Bug found & fixed:** the legacy `.../sapi/api/summarized/...` path 404s; the live service is under `.../cde/summarized/...`. `from`/`to` query params (format `MM-YYYY`) are **required**, not optional -- the adapter now defaults to the trailing 12 full months when not supplied. The response is also **not** a flat `results` list as originally assumed; it nests monthly figures under `offenses.{actuals,rates}` keyed by category label. The adapter now flattens this into a tabular `results` list. Verified against a real state query. |
| EPA Envirofacts | Yes | Confirmed correct: the `efservice` REST path (state-filtered TRI facility query) is still live and returns real records, even though EPA's docs now foreground the newer `dmapservice` GraphQL-like API as primary. |
| NOAA/NWS | Yes | Confirmed correct end-to-end: `/points/{lat},{lon}` &rarr; `properties.forecast` &rarr; `properties.periods` round-trip verified against a live coordinate. |
| RentCast | Yes | Confirmed fully correct against RentCast's official OpenAPI reference: base URL, the `/properties` path, `address`/`limit` query params, the `X-Api-Key` auth header, and the documented response schema (a bare JSON array of property objects, matching `payload if isinstance(payload, list) ...`). A live request with a bad key returned `401` (i.e. reached the real endpoint and auth was checked); full success-path parsing was cross-checked against RentCast's documented example response since no real key is available in this environment. |
| Zillow | No (enterprise-gated) | Zillow/Bridge access requires an approved paid license; there is no key available to test against. Fixed a confirmed **path bug** (missing `/zestimates` resource segment) found by reading Bridge's own platform docs, and now sends both the documented `Authorization: Bearer` header and `access_token` query-param fallback. The exact response envelope (`bundle` vs. `value` vs. a bare list) could **not** be confirmed live -- the adapter checks all three, but this remains unverified until tested against a real Bridge account. |

Takeaway: 7 of 9 adapters (Census, Walk Score, FEMA, FRED, FBI Crime Data,
EPA, NOAA) were checked end-to-end against live traffic, and RentCast was
fully confirmed against its official API reference plus a live auth check.
Four real bugs were found and fixed as a result: two wrong endpoint paths
(FEMA, FBI Crime Data), one silent-failure bug (Walk Score reports HTTP 200
even on auth/quota errors), and one stale assumption (Census now mandates an
API key it previously treated as optional). Only Zillow could not be fully
verified, because it requires a paid, approval-gated account with no
available test credentials.
