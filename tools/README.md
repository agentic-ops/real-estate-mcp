# Tools

Each module exposes a `register_<category>_tools(mcp)` function; the package
`__init__.py` wires them together in `register_all_tools(mcp)`, gated by the
`REALESTATE_MCP_ENABLE_*` feature flags (see `feature_flags.py`).

| Module | Category flag | Purpose |
|--------|---------------|---------|
| `property_tools.py` | `property` | Search, filter, area listings, property insights |
| `agent_tools.py` | `agent` | Agent profiles, portfolios, dashboards |
| `market_tools.py` | `market` | Market overview, price analytics, comparisons, sales |
| `client_tools.py` | `client` | Client profiles and preference matching |
| `area_tools.py` | `area` | Area reports, schools, parks, shopping, healthcare |
| `mortgage_tools.py` | `mortgage` | Payment, amortization, affordability, refinance |
| `valuation_tools.py` | `valuation` | Comparable valuation + investment metrics |
| `deep_analysis_tools.py` | `valuation` | MCP sampling deep analysis + heuristic fallback |
| `document_tools.py` | `document` | Listing ingestion + `.docx` report export |
| `analysis_queue_tools.py` | `analysis_queue` | SQLite-backed async analysis queue |
| `integration_tools.py` | `integrations` | Live integration status + lookups (free: Census, Walk Score, FEMA, FRED, FBI Crime, EPA, NOAA; paid: RentCast, Zillow) |
| `system_tools.py` | `system` | Data refresh, server info, summaries |

Shared helper: `finance_helpers.py` holds the pure, deterministic finance
math (mortgage/amortization/affordability/investment) used by the mortgage and
valuation tools. Keep it side-effect-free so it stays exactly unit-testable.

## Conventions

- Tools return `json.dumps(..., indent=2)` strings.
- Call `audit(...)` (from `utils`) at the top of each tool for provenance.
- Keep tools deterministic and offline; live network access belongs only in
  the opt-in `integrations/` adapters.
- Never echo secrets (API keys) back in tool output.
