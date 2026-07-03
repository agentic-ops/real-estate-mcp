# AGENTS.md

Guidance for AI agents and developers working in this repository.

## What this is

A Model Context Protocol (MCP) server for real estate workflows: property
search and insights, agent/client management, market and area intelligence,
mortgage/affordability math, comparable-based valuation, investment analysis,
and listing-document ingestion — plus optional opt-in live integrations
(Census, RentCast). See `README.md` for the full feature list and
`WORKFLOW_EXAMPLES.md` for end-to-end examples.

## Project layout

- `main.py` — FastMCP entry point; exposes a module-level `mcp` object and a
  `create_server()` factory. Registers everything and runs the transport.
- `utils.py` — `RealEstateDataManager` (loads `data/**/*.json`), plus `audit()`
  and the `get_data_manager()` process-wide singleton. The `data_manager`
  global is retained for backward compatibility.
- `feature_flags.py` — category-level `REALESTATE_MCP_ENABLE_*` flags.
- `tools/`, `resources/`, `prompts/` — each module has a `register_*`
  function; the package `__init__.py` wires them together
  (`register_all_tools`, `register_all_resources`, `register_all_prompts`).
- `tools/finance_helpers.py` — pure, deterministic finance math (unit-tested).
- `integrations/` — `config.py` (feature flags + credentials from env),
  `census.py`, `rentcast.py`. Disabled by default.
- `data/` — JSON seed data. Adding/adjusting data usually requires no code
  changes.
- `tests/` — `unit/` and `integration/`; shared helpers in `tests/conftest.py`
  (`call_tool_json`, `read_resource_json`, `mcp_server`).

## How to run / test / lint (standard commands)

Commands are documented in `README.md` (Quick start + Testing sections) and
`requirements.txt`. In short: `python main.py` to run (stdio by default);
`pytest`, `python -m black .`, `python -m flake8 .`, `python -m mypy .` for
checks.

## Conventions

- Tools/resources return `json.dumps(..., indent=2)` strings and call
  `audit(...)` for provenance.
- Keep the core deterministic and offline; live network access only through
  the opt-in `integrations/` adapters.
- Never echo secrets (API tokens) back in tool/resource output — see the
  `status()` methods for the safe pattern.
- Preserve v1 tool names and resource URIs; `tests/integration/test_server.py`
  guards backward compatibility.

## Cursor Cloud specific instructions

- **Dependencies** are installed by the startup update script (`pip install -r
  requirements.txt`, user site-packages). You normally do not need to install
  anything manually.
- **PATH gotcha:** console scripts (`pytest`, `black`, `flake8`, `mypy`,
  `uvicorn`, `mcp`) install to `~/.local/bin`, which is not on `PATH` by
  default. Invoke them as `python3 -m pytest`, `python3 -m black .`, etc., or
  prepend `~/.local/bin` to `PATH`.
- **Default transport is stdio** (for Claude Desktop compatibility). For local
  browser/HTTP testing, start SSE explicitly in a long-lived tmux session:
  `python3 main.py --transport sse` (endpoints `/sse` and `/messages/` on
  `127.0.0.1:8000`). Bind `0.0.0.0` (`HOST=0.0.0.0`) only if something outside
  the VM needs to reach it.
- **MCP Inspector (browser test):** run
  `DANGEROUSLY_OMIT_AUTH=true MCP_AUTO_OPEN_ENABLED=false npx -y
  @modelcontextprotocol/inspector`. UI serves on `localhost:6274`, proxy on
  `6277` (both bind IPv6 `::1`, so use `localhost`, not `127.0.0.1`). Connect
  with Transport = SSE, URL = `http://127.0.0.1:8000/sse`.
- **Live integrations are OFF by default** and must stay that way in tests.
  RentCast is metered and may incur costs; do not enable it against production.
  The test suite mocks `httpx` (`httpx.MockTransport`) so no real network calls
  occur — keep new integration tests network-free the same way.
- **Analysis queue writes a local SQLite file** (`real_estate_mcp_analysis.db`)
  in the working directory; it is gitignored. Tests point `_DB_PATH` at a temp
  file via monkeypatch, so never commit a stray `.db`.
- **After editing code, restart the running server** to pick up changes (there
  is no auto-reload in this setup).
- **`.venv` note:** creating a venv needs the `python3.12-venv` system package,
  which may be absent. The supported path is user-level `pip install`, not a
  venv.
