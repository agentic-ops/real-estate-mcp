# Real Estate MCP Server

A comprehensive Model Context Protocol (MCP) server for real estate
workflows. It provides tools, resources, and prompts for property listings,
agent management, market analysis, client relationships, area intelligence,
**mortgage/affordability math, comparable-based valuation, investment
analysis, listing-document ingestion**, and optional **opt-in live data
integrations** (Census, RentCast).

> **Version 2.0.0** — a major build-out over v1: 50+ tools across 11
> feature-flagged categories, deterministic finance/valuation engines, an
> async analysis queue, MCP sampling support, Docker packaging, and a much
> larger automated test suite. All v1 tool names and resource URIs are
> preserved for backward compatibility.

---

## Table of Contents

- [Highlights](#highlights)
- [Architecture](#architecture)
- [Quick start](#quick-start)
- [Running the server](#running-the-server)
- [Tool categories](#tool-categories)
- [Resources](#resources)
- [Prompts](#prompts)
- [Feature flags](#feature-flags)
- [Optional live integrations](#optional-live-integrations)
- [Docker](#docker)
- [Testing](#testing)
- [Linting & type checking](#linting--type-checking)
- [Development](#development)
- [Integration & development support](#integration--development-support)
- [License](#license)

---

## Highlights

- **50+ Tools** across property, agent, market, client, area, mortgage,
  valuation, document, analysis-queue, integration, and system categories.
- **Deterministic finance engine** (`tools/finance_helpers.py`): mortgage
  payments, amortization schedules, affordability, and investment metrics —
  pure functions, fully unit-tested.
- **Comparable-based valuation** using the local sales data (CMA-style).
- **Listing-document ingestion** of `.txt`/`.docx` files with `.docx` report
  export (`python-docx`).
- **Async analysis queue** backed by SQLite for batch listing analysis.
- **MCP sampling** support: `deep_analyze_property` asks the connected
  client's LLM for deeper reasoning, with a deterministic heuristic fallback.
- **Feature flags**: disable entire tool categories via environment variables.
- **Opt-in live integrations** (Census, RentCast) — **off by default** and
  network-free in tests.
- **Multiple transports**: `stdio` (default), `sse`, and `streamable-http`.

## Architecture

```
real-estate-mcp/
├── main.py                    # create_server() factory + transport CLI
├── utils.py                   # RealEstateDataManager, audit(), get_data_manager()
├── feature_flags.py           # category-level REALESTATE_MCP_ENABLE_* flags
├── tools/                     # MCP tools (one register_* per module)
│   ├── property_tools.py      # search, filter, insights
│   ├── agent_tools.py         # profiles, dashboards
│   ├── market_tools.py        # market analytics, sales
│   ├── client_tools.py        # client management + matching
│   ├── area_tools.py          # area intelligence + amenities
│   ├── mortgage_tools.py      # payment, amortization, affordability, refinance
│   ├── valuation_tools.py     # CMA valuation + investment analysis
│   ├── document_tools.py      # listing ingestion + .docx report export
│   ├── analysis_queue_tools.py# SQLite-backed async analysis queue
│   ├── deep_analysis_tools.py # MCP sampling with heuristic fallback
│   ├── integration_tools.py   # live integration status + lookups
│   ├── system_tools.py        # data refresh, server info, summaries
│   ├── finance_helpers.py     # shared, pure finance math
│   └── __init__.py            # register_all_tools() (feature-flagged)
├── resources/                 # MCP resources (config + domain data)
├── prompts/                   # MCP prompt templates
├── integrations/              # opt-in Census + RentCast adapters (off by default)
├── data/                      # JSON seed data
└── tests/                     # unit/ + integration/ (network-free)
```

## Quick start

```bash
# Clone
git clone https://github.com/agentic-ops/real-estate-mcp.git
cd real-estate-mcp

# (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install runtime + dev dependencies
pip install -r requirements.txt
# or, from pyproject: pip install -e ".[dev]"

# Run (stdio transport, ideal for Claude Desktop)
python main.py
```

### Claude Desktop

```json
{
  "mcpServers": {
    "real-estate": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/real-estate-mcp/main.py"],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

Or install via the MCP CLI: `mcp install main.py --name "Real Estate"`.

## Running the server

The default transport is **stdio** (unchanged from v1, for Claude Desktop).
Transport/host/port are configurable via flags or environment variables.

```bash
python main.py                       # stdio (default)
python main.py sse                   # legacy positional form (still supported)
python main.py --transport sse       # SSE on http://127.0.0.1:8000/sse
python main.py --transport streamable-http --host 0.0.0.0 --port 9000
```

Environment variables: `MCP_TRANSPORT`, `HOST`, `PORT`, `LOG_LEVEL`.

### MCP Inspector

```bash
# Load the module-level server object directly
mcp dev main.py:mcp

# Or point the Inspector at a running SSE server
DANGEROUSLY_OMIT_AUTH=true npx -y @modelcontextprotocol/inspector
# then connect: Transport = SSE, URL = http://127.0.0.1:8000/sse
```

## Tool categories

| Category | Env flag | Example tools |
|----------|----------|---------------|
| Property | `REALESTATE_MCP_ENABLE_PROPERTY` | `search_properties`, `filter_properties`, `get_property_insights` |
| Agent | `REALESTATE_MCP_ENABLE_AGENT` | `get_agent_dashboard`, `get_agent_sales` |
| Market | `REALESTATE_MCP_ENABLE_MARKET` | `get_market_overview`, `compare_areas` |
| Client | `REALESTATE_MCP_ENABLE_CLIENT` | `match_client_preferences` |
| Area | `REALESTATE_MCP_ENABLE_AREA` | `get_comprehensive_area_report`, `get_schools_data` |
| Mortgage | `REALESTATE_MCP_ENABLE_MORTGAGE` | `calculate_mortgage_payment`, `estimate_affordability_tool`, `compare_refinance` |
| Valuation | `REALESTATE_MCP_ENABLE_VALUATION` | `estimate_property_value`, `analyze_investment`, `deep_analyze_property` |
| Document | `REALESTATE_MCP_ENABLE_DOCUMENT` | `ingest_listing_document`, `export_property_report` |
| Analysis queue | `REALESTATE_MCP_ENABLE_ANALYSIS_QUEUE` | `queue_property_analysis`, `get_analysis_result` |
| Integrations | `REALESTATE_MCP_ENABLE_INTEGRATIONS` | `integration_status`, `lookup_live_property` |
| System | `REALESTATE_MCP_ENABLE_SYSTEM` | `get_server_info`, `refresh_data`, `get_data_summary` |

## Resources

Static resources (always available): `realestate://server-config`,
`realestate://all-properties`, `realestate://all-agents`,
`realestate://market-overview`, `realestate://all-areas`,
`realestate://amenities`, `realestate://integrations/status`.

Dynamic resource templates: `realestate://properties/area/{area}`,
`realestate://agent/{agent_id}/dashboard`, `realestate://market/area/{area}`,
`realestate://property/{property_id}/insights`,
`realestate://client/{client_id}/matches`.

## Prompts

13 prompt templates spanning property, client, market, agent, and finance
workflows (including `mortgage_planning_prompt` and `valuation_prompt`).

## Feature flags

Every tool category is **enabled by default**. Set the matching
`REALESTATE_MCP_ENABLE_*` variable to `false` (or `0`/`no`/`off`) to disable a
category before startup — its tools *and* matching resources are skipped.
The current state is reported by the `realestate://server-config` resource and
the `get_server_info` tool.

## Optional live integrations

Two adapters are available and **disabled by default**:

- **Census Bureau API** (`CENSUS_ENABLED`, optional `CENSUS_API_KEY`) — free,
  preferred for demographic context.
- **RentCast** (`RENTCAST_ENABLED`, `RENTCAST_API_KEY`) — **metered**; requests
  draw against a monthly quota and may incur costs.

When disabled or unconfigured, the integration tools/resources return a clear
status payload and make **no** network calls. Status output never echoes API
keys. See `.env.example` and `integrations/README.md`.

## Docker

```bash
docker compose up --build          # SSE on http://localhost:8000/sse
```

The container defaults to SSE and binds `0.0.0.0`. Integrations stay off
unless you pass the corresponding environment variables.

## Testing

```bash
pytest                             # full suite (unit + integration)
pytest tests/unit/                 # fast unit tests
pytest tests/integration/          # MCP tool/resource integration tests
python run_tests.py all -v -c      # convenience runner with coverage
```

The suite is **network-free**: live integrations are exercised with
`httpx.MockTransport` so no external calls occur. Tests cover the finance
engine, feature flags, every new tool category, integration adapters, config
resources, and v1 backward compatibility.

## Linting & type checking

```bash
python -m black .                  # format
python -m flake8 .                 # style
python -m mypy .                   # type check (source; tests excluded)
```

> On some systems console scripts install to `~/.local/bin`, which may not be
> on `PATH`. Invoke tools as `python -m pytest`, `python -m black .`, etc.

## Development

Add a tool by writing a `register_*` function in the appropriate
`tools/*.py`, wiring it into `tools/__init__.py` under the right feature-flag
category, and adding tests under `tests/`. Tools return
`json.dumps(..., indent=2)` strings and call `audit(...)` for provenance.
Keep the core deterministic and offline — live network access belongs only in
the opt-in `integrations/` adapters.

## Integration & development support

Need help integrating this real estate MCP server into your brokerage or
agency workflows, enabling the Census or RentCast adapters, or building custom
real estate MCP tools and extensions? Professional integration and development
support is available.

- **Email:** edwin@genego.io
- **LinkedIn:** [Edwin Genego](https://www.linkedin.com/in/edwingenego)

We're happy to help with deployment, custom integrations, and tailored real
estate workflow automation.

## License

GNU Affero General Public License v3.0 (AGPL-3.0) — see [LICENSE](LICENSE).

Free to use, fork, and self-host. If you run a modified version as a network
service, AGPL-3.0 requires you to publish your changes. Organizations that need
to keep modifications private can contact **edwin@genego.io** for a commercial
license.

---

*Built with the Model Context Protocol (MCP). Provides workflow augmentation,
not financial, legal, or appraisal advice.*
