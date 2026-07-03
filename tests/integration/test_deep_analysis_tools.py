"""Integration tests for the sampling-based deep analysis tool.

Without a connected client that advertises sampling capability, the tool
must gracefully fall back to deterministic heuristic-only output.
"""

from tests.conftest import call_tool_json


class TestDeepAnalysis:
    async def test_heuristic_fallback_for_real_listing(self, mcp_server):
        result = await call_tool_json(
            mcp_server, "deep_analyze_property", {"property_id": "PROP001"}
        )
        assert result["property_id"] == "PROP001"
        assert result["heuristic_analysis"]["area"]
        # No sampling-capable client in tests -> LLM reasoning is absent.
        assert result["llm_reasoning"] is None
        assert "note" in result

    async def test_missing_property(self, mcp_server):
        result = await call_tool_json(
            mcp_server, "deep_analyze_property", {"property_id": "NOPE"}
        )
        assert "error" in result
