"""
Integration tests for property tools
"""

import pytest
import json
from unittest.mock import Mock, patch

from tools.property_tools import register_property_tools
from utils import data_manager


class TestPropertyTools:
    """Test property-related MCP tools"""
    
    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register tools"""
        mcp = Mock()
        tools = {}
        
        def mock_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator
        
        mcp.tool = mock_tool
        register_property_tools(mcp)
        return tools
    
    def test_get_all_properties(self, mock_mcp, test_data_manager):
        """Test get_all_properties tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['get_all_properties']()
            data = json.loads(result)
            
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] == "TEST001"
            assert data[1]["id"] == "TEST002"
    
    def test_get_property_details(self, mock_mcp, test_data_manager):
        """Test get_property_details tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            # Test existing property
            result = mock_mcp['get_property_details']("TEST001")
            data = json.loads(result)
            
            assert data["id"] == "TEST001"
            assert data["address"] == "123 Test St"
            assert data["price"] == 500000
            
            # Test non-existent property
            result = mock_mcp['get_property_details']("NONEXISTENT")
            assert "not found" in result.lower()
    
    def test_search_properties(self, mock_mcp, test_data_manager):
        """Test search_properties tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['search_properties']("Test St")
            data = json.loads(result)
            
            assert data["query"] == "Test St"
            assert data["results_count"] == 1
            assert len(data["properties"]) == 1
            assert data["properties"][0]["id"] == "TEST001"
    
    def test_filter_properties(self, mock_mcp, test_data_manager):
        """Test filter_properties tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['filter_properties'](
                min_price=400000,
                max_price=600000,
                min_bedrooms=3
            )
            data = json.loads(result)
            
            assert data["filters_applied"]["min_price"] == 400000
            assert data["filters_applied"]["max_price"] == 600000
            assert data["filters_applied"]["min_bedrooms"] == 3
            assert data["results_count"] == 1
            assert data["properties"][0]["id"] == "TEST001"
    
    def test_filter_properties_with_areas(self, mock_mcp, test_data_manager):
        """Test filter_properties tool with areas parameter"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['filter_properties'](
                areas="Test Area,Another Area"
            )
            data = json.loads(result)
            
            assert data["filters_applied"]["areas"] == ["Test Area", "Another Area"]
            assert data["results_count"] == 2  # Both properties are in Test Area
    
    def test_get_properties_by_area(self, mock_mcp, test_data_manager):
        """Test get_properties_by_area tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['get_properties_by_area']("Test Area")
            data = json.loads(result)
            
            assert data["area"] == "Test Area"
            assert data["properties_count"] == 2
            assert len(data["properties"]) == 2
    
    def test_get_property_insights(self, mock_mcp, test_data_manager):
        """Test get_property_insights tool"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['get_property_insights']("TEST001")
            data = json.loads(result)
            
            assert "property" in data
            assert data["property"]["id"] == "TEST001"
            assert "listing_agent" in data
            assert "area_context" in data
            assert "comparable_sales" in data
            
            # Test non-existent property
            result = mock_mcp['get_property_insights']("NONEXISTENT")
            assert "not found" in result.lower()
    
    def test_filter_properties_no_filters(self, mock_mcp, test_data_manager):
        """Test filter_properties tool with no filters applied"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['filter_properties']()
            data = json.loads(result)
            
            assert data["results_count"] == 2  # Should return all properties
            assert len(data["properties"]) == 2
    
    def test_search_properties_case_insensitive(self, mock_mcp, test_data_manager):
        """Test search_properties is case insensitive"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            result = mock_mcp['search_properties']("townhouse")  # lowercase
            data = json.loads(result)
            
            assert data["results_count"] == 1
            assert data["properties"][0]["property_type"] == "Townhouse"
    
    def test_filter_properties_edge_cases(self, mock_mcp, test_data_manager):
        """Test filter_properties with edge cases"""
        with patch('tools.property_tools.data_manager', test_data_manager):
            # Test with very high price filter (no results)
            result = mock_mcp['filter_properties'](min_price=2000000)
            data = json.loads(result)
            assert data["results_count"] == 0
            
            # Test with very low price filter (all results)
            result = mock_mcp['filter_properties'](max_price=1000000)
            data = json.loads(result)
            assert data["results_count"] == 2 