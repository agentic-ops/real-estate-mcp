# Tests

The suite is split into fast unit tests and MCP integration tests. It is
**network-free**: the optional integrations are exercised with
`httpx.MockTransport`, so running the tests never makes external calls.

```
tests/
├── conftest.py                       # fixtures + call_tool_json / read_resource_json helpers
├── unit/
│   ├── test_utils.py                 # RealEstateDataManager + PropertyFilter
│   ├── test_utils_extended.py        # stats(), get_data_manager(), audit()
│   ├── test_finance_helpers.py       # deterministic finance math
│   └── test_feature_flags.py         # category flag parsing
└── integration/
    ├── test_property_tools.py        # v1 property tools
    ├── test_all_tools.py             # v1 agent/market/client/area/system tools
    ├── test_resources.py             # v1 resources + templates
    ├── test_prompts.py               # prompt templates
    ├── test_mortgage_tools.py        # mortgage/affordability
    ├── test_valuation_tools.py       # valuation + investment
    ├── test_document_tools.py        # ingestion + .docx export
    ├── test_analysis_queue_tools.py  # async SQLite queue (temp DB)
    ├── test_deep_analysis_tools.py   # sampling fallback
    ├── test_integrations.py          # Census/RentCast adapters (mocked httpx)
    ├── test_config_resources.py      # server-config + integration resources
    └── test_server.py                # registration + v1 backward compatibility
```

## Running

```bash
pytest                          # everything
pytest tests/unit/              # fast unit tests
pytest tests/integration/       # integration tests
pytest -k mortgage              # by keyword
```

`pyproject.toml` sets `asyncio_mode = "auto"`, so async test functions run
without an explicit marker. Integration tests call tools through a real
`FastMCP` server built by `create_server()`.

## Conventions

- Use `call_tool_json(server, name, args)` and `read_resource_json(server, uri)`
  from `conftest.py` to invoke tools/resources and decode their JSON payloads.
- Keep new integration tests network-free (inject `httpx.MockTransport`).
- The analysis-queue tests point `_DB_PATH` at a temp file via monkeypatch so
  no database is written into the repo.
