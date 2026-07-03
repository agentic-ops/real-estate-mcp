"""Server-level registration and backward-compatibility tests.

These guard the promise that the v2 build-out does not remove or rename any
tool/resource that existing MCP clients already depend on.
"""

from main import create_server

# Tool names that shipped in v1 and must remain available.
LEGACY_TOOLS = {
    "get_all_properties",
    "get_property_details",
    "search_properties",
    "filter_properties",
    "get_properties_by_area",
    "get_property_insights",
    "get_all_agents",
    "get_agent_details",
    "search_agents",
    "get_agent_dashboard",
    "get_market_overview",
    "get_price_analytics",
    "compare_areas",
    "get_investment_opportunities",
    "get_all_clients",
    "match_client_preferences",
    "get_all_areas",
    "get_comprehensive_area_report",
    "refresh_data",
    "get_data_summary",
}

NEW_TOOLS = {
    "calculate_mortgage_payment",
    "estimate_affordability_tool",
    "estimate_property_value",
    "analyze_investment",
    "deep_analyze_property",
    "ingest_listing_document",
    "queue_property_analysis",
    "integration_status",
    "get_server_info",
}

LEGACY_RESOURCE_URIS = {
    "realestate://all-properties",
    "realestate://all-agents",
    "realestate://market-overview",
    "realestate://all-areas",
    "realestate://amenities",
}


async def _tool_names(server):
    return {t.name for t in await server.list_tools()}


class TestBackwardCompatibility:
    async def test_all_legacy_tools_present(self, mcp_server):
        names = await _tool_names(mcp_server)
        missing = LEGACY_TOOLS - names
        assert not missing, f"legacy tools removed: {missing}"

    async def test_new_tools_present(self, mcp_server):
        names = await _tool_names(mcp_server)
        missing = NEW_TOOLS - names
        assert not missing, f"new tools missing: {missing}"

    async def test_legacy_resource_uris_present(self, mcp_server):
        uris = {str(r.uri) for r in await mcp_server.list_resources()}
        missing = LEGACY_RESOURCE_URIS - uris
        assert not missing, f"legacy resources removed: {missing}"

    async def test_prompts_still_registered(self, mcp_server):
        prompts = await mcp_server.list_prompts()
        assert len(prompts) >= 11


class TestFeatureFlaggedRegistration:
    async def test_disabling_category_removes_tools(self, monkeypatch):
        monkeypatch.setenv("REALESTATE_MCP_ENABLE_MORTGAGE", "false")
        monkeypatch.setenv("REALESTATE_MCP_ENABLE_INTEGRATIONS", "false")
        server = create_server()
        names = await _tool_names(server)
        assert "calculate_mortgage_payment" not in names
        assert "integration_status" not in names
        # Unrelated categories remain.
        assert "search_properties" in names

    async def test_default_registers_full_surface(self, mcp_server):
        names = await _tool_names(mcp_server)
        assert len(names) >= 50
