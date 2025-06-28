"""
Unit tests for utils.py - RealEstateDataManager and PropertyFilter
"""

import pytest
import json
import os
from unittest.mock import patch, mock_open

from utils import RealEstateDataManager, PropertyFilter


class TestPropertyFilter:
    """Test PropertyFilter dataclass"""
    
    def test_property_filter_initialization(self):
        """Test PropertyFilter can be initialized with various parameters"""
        pf = PropertyFilter(
            min_price=100000,
            max_price=500000,
            min_bedrooms=2,
            max_bedrooms=4,
            areas=["Downtown", "Suburbs"],
            property_types=["House", "Condo"]
        )
        
        assert pf.min_price == 100000
        assert pf.max_price == 500000
        assert pf.min_bedrooms == 2
        assert pf.max_bedrooms == 4
        assert pf.areas == ["Downtown", "Suburbs"]
        assert pf.property_types == ["House", "Condo"]
    
    def test_property_filter_defaults(self):
        """Test PropertyFilter defaults to None for all fields"""
        pf = PropertyFilter()
        
        assert pf.min_price is None
        assert pf.max_price is None
        assert pf.min_bedrooms is None
        assert pf.max_bedrooms is None
        assert pf.areas is None
        assert pf.property_types is None


class TestRealEstateDataManager:
    """Test RealEstateDataManager class"""
    
    def test_initialization(self, test_data_manager):
        """Test data manager initializes correctly"""
        assert test_data_manager.data_dir is not None
        assert hasattr(test_data_manager, 'properties')
        assert hasattr(test_data_manager, 'agents')
        assert hasattr(test_data_manager, 'clients')
    
    def test_get_all_properties(self, test_data_manager):
        """Test getting all properties"""
        properties = test_data_manager.get_all_properties()
        assert isinstance(properties, list)
        assert len(properties) == 2
        assert properties[0]["id"] == "TEST001"
        assert properties[1]["id"] == "TEST002"
    
    def test_get_property_by_id(self, test_data_manager):
        """Test getting property by ID"""
        prop = test_data_manager.get_property_by_id("TEST001")
        assert prop is not None
        assert prop["id"] == "TEST001"
        assert prop["address"] == "123 Test St"
        
        # Test non-existent property
        prop = test_data_manager.get_property_by_id("NONEXISTENT")
        assert prop is None
    
    def test_search_properties(self, test_data_manager):
        """Test property search functionality"""
        # Search by address
        results = test_data_manager.search_properties("Test St")
        assert len(results) == 1
        assert results[0]["id"] == "TEST001"
        
        # Search by property type
        results = test_data_manager.search_properties("Townhouse")
        assert len(results) == 1
        assert results[0]["id"] == "TEST002"
        
        # Search by feature
        results = test_data_manager.search_properties("Pool")
        assert len(results) == 1
        assert results[0]["id"] == "TEST002"
        
        # Search with no results
        results = test_data_manager.search_properties("Nonexistent")
        assert len(results) == 0
    
    def test_filter_properties(self, test_data_manager):
        """Test property filtering functionality"""
        # Filter by price range
        filters = PropertyFilter(min_price=400000, max_price=600000)
        results = test_data_manager.filter_properties(filters)
        assert len(results) == 1
        assert results[0]["id"] == "TEST001"
        
        # Filter by bedrooms
        filters = PropertyFilter(min_bedrooms=3)
        results = test_data_manager.filter_properties(filters)
        assert len(results) == 1
        assert results[0]["id"] == "TEST001"
        
        # Filter by area
        filters = PropertyFilter(areas=["Test Area"])
        results = test_data_manager.filter_properties(filters)
        assert len(results) == 2
        
        # Filter with no matches
        filters = PropertyFilter(min_price=1000000)
        results = test_data_manager.filter_properties(filters)
        assert len(results) == 0
    
    def test_matches_filter_price(self, test_data_manager):
        """Test price filtering logic"""
        prop = {"price": 500000}
        
        # Test min price
        filters = PropertyFilter(min_price=400000)
        assert test_data_manager._matches_filter(prop, filters) is True
        
        filters = PropertyFilter(min_price=600000)
        assert test_data_manager._matches_filter(prop, filters) is False
        
        # Test max price
        filters = PropertyFilter(max_price=600000)
        assert test_data_manager._matches_filter(prop, filters) is True
        
        filters = PropertyFilter(max_price=400000)
        assert test_data_manager._matches_filter(prop, filters) is False
    
    def test_matches_filter_bedrooms(self, test_data_manager):
        """Test bedroom filtering logic"""
        prop = {"bedrooms": 3}
        
        # Test min bedrooms
        filters = PropertyFilter(min_bedrooms=2)
        assert test_data_manager._matches_filter(prop, filters) is True
        
        filters = PropertyFilter(min_bedrooms=4)
        assert test_data_manager._matches_filter(prop, filters) is False
        
        # Test max bedrooms
        filters = PropertyFilter(max_bedrooms=4)
        assert test_data_manager._matches_filter(prop, filters) is True
        
        filters = PropertyFilter(max_bedrooms=2)
        assert test_data_manager._matches_filter(prop, filters) is False
    
    def test_matches_filter_features(self, test_data_manager):
        """Test feature filtering logic"""
        prop = {"features": ["Garage", "Garden", "Swimming Pool"]}
        
        # Test single feature match
        filters = PropertyFilter(features=["Garage"])
        assert test_data_manager._matches_filter(prop, filters) is True
        
        # Test partial feature match
        filters = PropertyFilter(features=["Pool"])
        assert test_data_manager._matches_filter(prop, filters) is True
        
        # Test no feature match
        filters = PropertyFilter(features=["Basement"])
        assert test_data_manager._matches_filter(prop, filters) is False
        
        # Test multiple features
        filters = PropertyFilter(features=["Garage", "Garden"])
        assert test_data_manager._matches_filter(prop, filters) is True
    
    def test_get_properties_by_area(self, test_data_manager):
        """Test getting properties by area"""
        properties = test_data_manager.get_properties_by_area("Test Area")
        assert len(properties) == 2
        
        properties = test_data_manager.get_properties_by_area("Nonexistent Area")
        assert len(properties) == 0
    
    def test_get_properties_by_agent(self, test_data_manager):
        """Test getting properties by agent"""
        properties = test_data_manager.get_properties_by_agent("AGENT001")
        assert len(properties) == 1
        assert properties[0]["id"] == "TEST001"
        
        properties = test_data_manager.get_properties_by_agent("NONEXISTENT")
        assert len(properties) == 0
    
    def test_get_all_agents(self, test_data_manager):
        """Test getting all agents"""
        agents = test_data_manager.get_all_agents()
        assert isinstance(agents, list)
        assert len(agents) == 2
        assert agents[0]["id"] == "AGENT001"
        assert agents[1]["id"] == "AGENT002"
    
    def test_get_agent_by_id(self, test_data_manager):
        """Test getting agent by ID"""
        agent = test_data_manager.get_agent_by_id("AGENT001")
        assert agent is not None
        assert agent["id"] == "AGENT001"
        assert agent["name"] == "Test Agent 1"
        
        # Test non-existent agent
        agent = test_data_manager.get_agent_by_id("NONEXISTENT")
        assert agent is None
    
    def test_search_agents(self, test_data_manager):
        """Test agent search functionality"""
        # Search by name
        results = test_data_manager.search_agents("Test Agent 1")
        assert len(results) == 1
        assert results[0]["id"] == "AGENT001"
        
        # Search by specialization
        results = test_data_manager.search_agents("Luxury")
        assert len(results) == 1
        assert results[0]["id"] == "AGENT001"
        
        # Search with no results
        results = test_data_manager.search_agents("Nonexistent")
        assert len(results) == 0
    
    def test_get_all_clients(self, test_data_manager):
        """Test getting all clients"""
        clients = test_data_manager.get_all_clients()
        assert isinstance(clients, list)
        assert len(clients) == 1
        assert clients[0]["id"] == "CLI001"
    
    def test_get_client_by_id(self, test_data_manager):
        """Test getting client by ID"""
        client = test_data_manager.get_client_by_id("CLI001")
        assert client is not None
        assert client["id"] == "CLI001"
        assert client["name"] == "Test Client 1"
        
        # Test non-existent client
        client = test_data_manager.get_client_by_id("NONEXISTENT")
        assert client is None
    
    def test_refresh_data(self, test_data_manager):
        """Test data refresh functionality"""
        # Modify cache
        test_data_manager._cache["test"] = "value"
        assert "test" in test_data_manager._cache
        
        # Refresh data
        test_data_manager.refresh_data()
        assert "test" not in test_data_manager._cache
    
    def test_load_json_file_caching(self, test_data_manager, temp_data_dir):
        """Test JSON file loading with caching"""
        filepath = os.path.join(temp_data_dir, "properties", "active_listings.json")
        
        # First load
        data1 = test_data_manager._load_json_file(filepath)
        assert filepath in test_data_manager._cache
        
        # Second load should use cache
        data2 = test_data_manager._load_json_file(filepath)
        assert data1 is data2  # Same object reference
    
    def test_load_json_file_error_handling(self, test_data_manager):
        """Test JSON file loading error handling"""
        # Test non-existent file
        data = test_data_manager._load_json_file("nonexistent.json")
        assert data == {}
        
        # Test invalid JSON (mocked)
        with patch("builtins.open", mock_open(read_data="invalid json")):
            data = test_data_manager._load_json_file("invalid.json")
            assert data == {} 