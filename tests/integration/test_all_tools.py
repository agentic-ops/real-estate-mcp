"""
Integration tests for all MCP tools
"""

import json
from unittest.mock import Mock, patch

import pytest

from tools.agent_tools import register_agent_tools
from tools.area_tools import register_area_tools
from tools.client_tools import register_client_tools
from tools.market_tools import register_market_tools
from tools.system_tools import register_system_tools


class TestAgentTools:
    """Test agent-related MCP tools"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register agent tools"""
        mcp = Mock()
        tools = {}

        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = mock_tool
        register_agent_tools(mcp)
        return tools

    def test_get_all_agents(self, mock_mcp, test_data_manager):
        """Test get_all_agents tool"""
        with patch("tools.agent_tools.data_manager", test_data_manager):
            result = mock_mcp["get_all_agents"]()
            data = json.loads(result)

            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "AGENT001"

    def test_get_agent_details(self, mock_mcp, test_data_manager):
        """Test get_agent_details tool"""
        with patch("tools.agent_tools.data_manager", test_data_manager):
            result = mock_mcp["get_agent_details"]("AGENT001")
            data = json.loads(result)

            assert data["id"] == "AGENT001"
            assert data["name"] == "Test Agent 1"

    def test_search_agents(self, mock_mcp, test_data_manager):
        """Test search_agents tool"""
        with patch("tools.agent_tools.data_manager", test_data_manager):
            result = mock_mcp["search_agents"]("Luxury")
            data = json.loads(result)

            assert data["query"] == "Luxury"
            assert data["results_count"] == 1
            assert data["agents"][0]["id"] == "AGENT001"


class TestMarketTools:
    """Test market-related MCP tools"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register market tools"""
        mcp = Mock()
        tools = {}

        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = mock_tool
        register_market_tools(mcp)
        return tools

    def test_get_market_overview(self, mock_mcp, test_data_manager):
        """Test get_market_overview tool"""
        with patch("tools.market_tools.data_manager", test_data_manager):
            result = mock_mcp["get_market_overview"]()
            data = json.loads(result)

            # The function returns the market overview data directly
            assert "average_price" in data or "market_overview" in data
            assert isinstance(data, dict)

    def test_get_area_market_data(self, mock_mcp, test_data_manager):
        """Test get_area_market_data tool"""
        with patch("tools.market_tools.data_manager", test_data_manager):
            result = mock_mcp["get_area_market_data"]("Test Area")
            # This might return None for test data, so we check for proper handling
            assert result is not None


class TestClientTools:
    """Test client-related MCP tools"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register client tools"""
        mcp = Mock()
        tools = {}

        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = mock_tool
        register_client_tools(mcp)
        return tools

    def test_get_all_clients(self, mock_mcp, test_data_manager):
        """Test get_all_clients tool"""
        with patch("tools.client_tools.data_manager", test_data_manager):
            result = mock_mcp["get_all_clients"]()
            data = json.loads(result)

            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["id"] == "CLI001"

    def test_get_client_details(self, mock_mcp, test_data_manager):
        """Test get_client_details tool"""
        with patch("tools.client_tools.data_manager", test_data_manager):
            result = mock_mcp["get_client_details"]("CLI001")
            data = json.loads(result)

            assert data["id"] == "CLI001"
            assert data["name"] == "Test Client 1"

    def test_match_client_preferences(self, mock_mcp, test_data_manager):
        """Test match_client_preferences tool"""
        with patch("tools.client_tools.data_manager", test_data_manager):
            result = mock_mcp["match_client_preferences"]("CLI001")
            data = json.loads(result)

            assert data["client_id"] == "CLI001"
            assert "matching_properties" in data


class TestAreaTools:
    """Test area-related MCP tools"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register area tools"""
        mcp = Mock()
        tools = {}

        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = mock_tool
        register_area_tools(mcp)
        return tools

    def test_get_area_details(self, mock_mcp, test_data_manager):
        """Test get_area_details tool"""
        with patch("tools.area_tools.data_manager", test_data_manager):
            result = mock_mcp["get_area_details"]("Test Area")
            # May return None for test data
            assert result is not None

    def test_get_area_amenities(self, mock_mcp, test_data_manager):
        """Test get_area_amenities tool"""
        with patch("tools.area_tools.data_manager", test_data_manager):
            result = mock_mcp["get_area_amenities"]("Test Area")
            data = json.loads(result)

            assert data["area"] == "Test Area"
            assert "amenities" in data

    def test_get_schools_data(self, mock_mcp, test_data_manager):
        """Test get_schools_data tool"""
        with patch("tools.area_tools.data_manager", test_data_manager):
            result = mock_mcp["get_schools_data"]()
            data = json.loads(result)

            assert isinstance(data, dict)


class TestSystemTools:
    """Test system-related MCP tools"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register system tools"""
        mcp = Mock()
        tools = {}

        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = mock_tool
        register_system_tools(mcp)
        return tools

    def test_refresh_data(self, mock_mcp, test_data_manager):
        """Test refresh_data tool"""
        with patch("tools.system_tools.data_manager", test_data_manager):
            result = mock_mcp["refresh_data"]()

            assert "refreshed successfully" in result

    def test_get_data_summary(self, mock_mcp, test_data_manager):
        """Test get_data_summary tool"""
        with patch("tools.system_tools.data_manager", test_data_manager):
            result = mock_mcp["get_data_summary"]()
            data = json.loads(result)

            assert "properties" in data
            assert "agents" in data
            assert "clients" in data
            assert data["properties"]["total_active_listings"] == 2
            assert data["agents"]["total_agents"] == 2
            assert data["clients"]["total_clients"] == 1
