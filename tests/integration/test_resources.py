"""
Integration tests for MCP resources
"""

import json
from unittest.mock import Mock, patch

import pytest

from resources import (
    register_agent_resources,
    register_client_resources,
    register_location_resources,
    register_market_resources,
    register_property_resources,
)


class TestPropertyResources:
    """Test property-related MCP resources"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register property resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource
        register_property_resources(mcp)
        return resources

    def test_get_all_properties_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-properties resource"""
        with patch("resources.property_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://all-properties"]()
            data = json.loads(result)

            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "TEST001"

    def test_get_properties_by_area_template(self, mock_mcp, test_data_manager):
        """Test realestate://properties/area/{area} template"""
        with patch("resources.property_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://properties/area/{area}"]("Test Area")
            data = json.loads(result)

            assert data["area"] == "Test Area"
            assert data["properties_count"] == 2
            assert len(data["properties"]) == 2

    def test_get_property_insights_template(self, mock_mcp, test_data_manager):
        """Test realestate://property/{property_id}/insights template"""
        with patch("resources.property_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://property/{property_id}/insights"]("TEST001")
            data = json.loads(result)

            assert "property" in data
            assert "area_context" in data
            assert "comparable_sales" in data
            assert data["property"]["id"] == "TEST001"

    def test_property_insights_nonexistent(self, mock_mcp, test_data_manager):
        """Test property insights with non-existent property"""
        with patch("resources.property_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://property/{property_id}/insights"](
                "NONEXISTENT"
            )
            data = json.loads(result)
            assert "error" in data


class TestAgentResources:
    """Test agent-related MCP resources"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register agent resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource
        register_agent_resources(mcp)
        return resources

    def test_get_all_agents_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-agents resource"""
        with patch("resources.agent_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://all-agents"]()
            data = json.loads(result)

            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "AGENT001"

    def test_get_agent_dashboard_template(self, mock_mcp, test_data_manager):
        """Test realestate://agent/{agent_id}/dashboard template"""
        with patch("resources.agent_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://agent/{agent_id}/dashboard"]("AGENT001")
            data = json.loads(result)

            assert "agent_info" in data
            assert "performance_metrics" in data
            assert "active_listings" in data
            assert data["agent_info"]["id"] == "AGENT001"

    def test_agent_dashboard_nonexistent(self, mock_mcp, test_data_manager):
        """Test agent dashboard with non-existent agent"""
        with patch("resources.agent_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://agent/{agent_id}/dashboard"]("NONEXISTENT")
            data = json.loads(result)
            assert "error" in data


class TestMarketResources:
    """Test market-related MCP resources"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register market resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource
        register_market_resources(mcp)
        return resources

    def test_get_market_overview_resource(self, mock_mcp, test_data_manager):
        """Test realestate://market-overview resource"""
        with patch("resources.market_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://market-overview"]()
            data = json.loads(result)

            # The resource returns market data directly
            assert isinstance(data, dict)
            assert "average_price" in data or "market_overview" in data

    def test_get_area_market_analysis_template(self, mock_mcp, test_data_manager):
        """Test realestate://market/area/{area} template"""
        with patch("resources.market_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://market/area/{area}"]("Test Area")
            data = json.loads(result)

            assert data["area"] == "Test Area"
            assert "market_data" in data
            assert "recent_sales" in data
            assert "area_info" in data


class TestClientResources:
    """Test client-related MCP resources"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register client resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource
        register_client_resources(mcp)
        return resources

    def test_get_client_matches_template(self, mock_mcp, test_data_manager):
        """Test realestate://client/{client_id}/matches template"""
        with patch("resources.client_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://client/{client_id}/matches"]("CLI001")
            data = json.loads(result)

            assert data["client_id"] == "CLI001"
            assert "matching_properties" in data

    def test_client_matches_nonexistent(self, mock_mcp, test_data_manager):
        """Test client matches with non-existent client"""
        with patch("resources.client_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://client/{client_id}/matches"]("NONEXISTENT")
            data = json.loads(result)
            assert "error" in data


class TestLocationResources:
    """Test location-related MCP resources"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register location resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource
        register_location_resources(mcp)
        return resources

    def test_get_all_areas_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-areas resource"""
        with patch("resources.location_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://all-areas"]()
            data = json.loads(result)

            assert isinstance(data, list)

    def test_get_amenities_resource(self, mock_mcp, test_data_manager):
        """Test realestate://amenities resource"""
        with patch("resources.location_resources.data_manager", test_data_manager):
            result = mock_mcp["realestate://amenities"]()
            data = json.loads(result)

            assert "schools" in data
            assert "parks_and_recreation" in data


class TestAllResources:
    """Test all resources together"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register all resources"""
        mcp = Mock()
        resources = {}

        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func

            return decorator

        mcp.resource = mock_resource

        # Register all resource modules
        register_property_resources(mcp)
        register_agent_resources(mcp)
        register_market_resources(mcp)
        register_client_resources(mcp)
        register_location_resources(mcp)

        return resources

    def test_all_resources_registered(self, mock_mcp):
        """Test that all expected resources are registered"""
        expected_resources = [
            "realestate://all-properties",
            "realestate://properties/area/{area}",
            "realestate://property/{property_id}/insights",
            "realestate://all-agents",
            "realestate://agent/{agent_id}/dashboard",
            "realestate://market-overview",
            "realestate://market/area/{area}",
            "realestate://client/{client_id}/matches",
            "realestate://all-areas",
            "realestate://amenities",
        ]

        for resource_uri in expected_resources:
            assert resource_uri in mock_mcp, f"Resource {resource_uri} not registered"

    def test_resource_count(self, mock_mcp):
        """Test that we have the expected number of resources"""
        assert len(mock_mcp) == 10, f"Expected 10 resources, got {len(mock_mcp)}"
