"""Integration tests for configuration and integration resources."""

from tests.conftest import read_resource_json


class TestConfigResource:
    async def test_server_config_resource(self, mcp_server):
        data = await read_resource_json(mcp_server, "realestate://server-config")
        assert "enabled_categories" in data
        assert "environment_variables" in data
        assert "data_stats" in data
        assert data["environment_variables"]["mortgage"] == (
            "REALESTATE_MCP_ENABLE_MORTGAGE"
        )

    async def test_integration_status_resource(self, mcp_server):
        data = await read_resource_json(mcp_server, "realestate://integrations/status")
        assert "census" in data
        assert "rentcast" in data
        # Never leaks secrets: only booleans / metadata.
        assert data["rentcast"]["enabled"] in (True, False)
