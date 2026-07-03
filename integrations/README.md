# Integrations

Optional adapters for external real-estate data providers. **All integrations
are disabled by default** and enabled per-integration via environment
variables. When disabled or unconfigured, the adapters return a structured
status payload and make **no** network calls.

| Module | Enable flag | Credentials | Cost |
|--------|-------------|-------------|------|
| `census.py` | `CENSUS_ENABLED` | `CENSUS_API_KEY` (optional) | Free (rate-limited) |
| `rentcast.py` | `RENTCAST_ENABLED` | `RENTCAST_API_KEY` (required) | Metered; may incur cost |

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

# Metered property data (understand the billing implications first)
export RENTCAST_ENABLED=true
export RENTCAST_API_KEY=...
```

See `.env.example` for the full list.
