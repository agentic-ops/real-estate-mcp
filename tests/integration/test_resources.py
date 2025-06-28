"""
Integration tests for MCP resources
"""

import pytest
import json
from unittest.mock import Mock, patch

from resources.static_resources import register_static_resources
from resources.resource_templates import register_resource_templates


class TestStaticResources:
    """Test static MCP resources"""
    
    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register static resources"""
        mcp = Mock()
        resources = {}
        
        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func
            return decorator
        
        mcp.resource = mock_resource
        register_static_resources(mcp)
        return resources
    
    def test_get_all_properties_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-properties resource"""
        with patch('resources.static_resources.data_manager', test_data_manager):
            result = mock_mcp['realestate://all-properties']()
            data = json.loads(result)
            
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "TEST001"
    
    def test_get_all_agents_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-agents resource"""
        with patch('resources.static_resources.data_manager', test_data_manager):
            result = mock_mcp['realestate://all-agents']()
            data = json.loads(result)
            
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "AGENT001"
    
    def test_get_market_overview_resource(self, mock_mcp, test_data_manager):
        """Test realestate://market-overview resource"""
        with patch('resources.static_resources.data_manager', test_data_manager):
            result = mock_mcp['realestate://market-overview']()
            data = json.loads(result)
            
            # The resource returns market data directly
            assert isinstance(data, dict)
            assert "average_price" in data or "market_overview" in data
    
    def test_get_all_areas_resource(self, mock_mcp, test_data_manager):
        """Test realestate://all-areas resource"""
        with patch('resources.static_resources.data_manager', test_data_manager):
            result = mock_mcp['realestate://all-areas']()
            data = json.loads(result)
            
            assert isinstance(data, list)
    
    def test_get_amenities_resource(self, mock_mcp, test_data_manager):
        """Test realestate://amenities resource"""
        with patch('resources.static_resources.data_manager', test_data_manager):
            result = mock_mcp['realestate://amenities']()
            data = json.loads(result)
            
            assert "schools" in data
            assert "parks_and_recreation" in data


class TestResourceTemplates:
    """Test template MCP resources"""
    
    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register resource templates"""
        mcp = Mock()
        resources = {}
        
        def mock_resource(uri):
            def decorator(func):
                resources[uri] = func
                return func
            return decorator
        
        mcp.resource = mock_resource
        register_resource_templates(mcp)
        return resources
    
    def test_get_properties_by_area_template(self, mock_mcp, test_data_manager):
        """Test realestate://properties/area/{area} template"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            result = mock_mcp['realestate://properties/area/{area}']("Test Area")
            data = json.loads(result)
            
            assert data["area"] == "Test Area"
            assert data["properties_count"] == 2
            assert len(data["properties"]) == 2
    
    def test_get_agent_dashboard_template(self, mock_mcp, test_data_manager):
        """Test realestate://agent/{agent_id}/dashboard template"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            result = mock_mcp['realestate://agent/{agent_id}/dashboard']("AGENT001")
            data = json.loads(result)
            
            assert "agent_info" in data
            assert "performance_metrics" in data
            assert "active_listings" in data
            assert data["agent_info"]["id"] == "AGENT001"
    
    def test_get_area_market_analysis_template(self, mock_mcp, test_data_manager):
        """Test realestate://market/area/{area} template"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            result = mock_mcp['realestate://market/area/{area}']("Test Area")
            data = json.loads(result)
            
            assert data["area"] == "Test Area"
            assert "market_data" in data
            assert "recent_sales" in data
            assert "area_info" in data
    
    def test_get_property_insights_template(self, mock_mcp, test_data_manager):
        """Test realestate://property/{property_id}/insights template"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            result = mock_mcp['realestate://property/{property_id}/insights']("TEST001")
            data = json.loads(result)
            
            assert "property" in data
            assert "area_context" in data
            assert "comparable_sales" in data
            assert data["property"]["id"] == "TEST001"
    
    def test_get_client_matches_template(self, mock_mcp, test_data_manager):
        """Test realestate://client/{client_id}/matches template"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            result = mock_mcp['realestate://client/{client_id}/matches']("CLI001")
            data = json.loads(result)
            
            assert data["client_id"] == "CLI001"
            assert "matching_properties" in data
    
    def test_template_with_nonexistent_data(self, mock_mcp, test_data_manager):
        """Test templates with non-existent data"""
        with patch('resources.resource_templates.data_manager', test_data_manager):
            # Test non-existent area
            result = mock_mcp['realestate://properties/area/{area}']("Nonexistent Area")
            data = json.loads(result)
            assert data["properties_count"] == 0
            
            # Test non-existent agent - this will return an error message
            result = mock_mcp['realestate://agent/{agent_id}/dashboard']("NONEXISTENT")
            data = json.loads(result)
            assert "error" in data
            
            # Test non-existent client
            result = mock_mcp['realestate://client/{client_id}/matches']("NONEXISTENT")
            data = json.loads(result)
            assert "error" in data 