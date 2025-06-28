"""
Pytest configuration and shared fixtures for the Real Estate MCP Server tests
"""

import pytest
import json
import os
import tempfile
from typing import Dict, Any
from unittest.mock import Mock, patch

from utils import RealEstateDataManager, PropertyFilter
from mcp.server.fastmcp import FastMCP


@pytest.fixture
def sample_properties():
    """Sample property data for testing"""
    return [
        {
            "id": "TEST001",
            "address": "123 Test St",
            "city": "Test City",
            "area": "Test Area",
            "property_type": "Single Family Home",
            "price": 500000,
            "bedrooms": 3,
            "bathrooms": 2.5,
            "square_feet": 2000,
            "features": ["Garage", "Garden"],
            "agent_id": "AGENT001"
        },
        {
            "id": "TEST002",
            "address": "456 Test Ave",
            "city": "Test City",
            "area": "Test Area",
            "property_type": "Townhouse",
            "price": 350000,
            "bedrooms": 2,
            "bathrooms": 2,
            "square_feet": 1500,
            "features": ["Pool", "Gym"],
            "agent_id": "AGENT002"
        }
    ]


@pytest.fixture
def sample_agents():
    """Sample agent data for testing"""
    return [
        {
            "id": "AGENT001",
            "name": "Test Agent 1",
            "specializations": ["Luxury Homes"],
            "expertise_areas": ["Test Area"],
            "years_experience": 10,
            "total_sales": 50
        },
        {
            "id": "AGENT002",
            "name": "Test Agent 2",
            "specializations": ["First-time Buyers"],
            "expertise_areas": ["Test Area"],
            "years_experience": 5,
            "total_sales": 25
        }
    ]


@pytest.fixture
def sample_clients():
    """Sample client data for testing"""
    return [
        {
            "id": "CLI001",
            "name": "Test Client 1",
            "type": "Buyer",
            "preferences": {
                "budget_range": {
                    "min": 400000,
                    "max": 600000
                },
                "desired_areas": ["Test Area"],
                "property_type": "Single Family Home",
                "bedrooms_min": 3
            }
        }
    ]


@pytest.fixture
def sample_market_data():
    """Sample market data for testing"""
    return {
        "market_overview": {
            "total_listings": 100,
            "average_price": 500000,
            "median_price": 450000,
            "market_type": "balanced",
            "avg_days_on_market": 30
        },
        "areas": {
            "Test Area": {
                "average_price": 500000,
                "total_listings": 50,
                "price_trend": "stable"
            }
        }
    }


@pytest.fixture
def sample_amenities():
    """Sample amenities data for testing"""
    return {
        "schools": {
            "Elementary": [
                {
                    "name": "Test Elementary",
                    "type": "Elementary",
                    "area": "Test Area",
                    "rating": 8
                }
            ]
        },
        "parks_and_recreation": {
            "parks": [
                {
                    "name": "Test Park",
                    "area": "Test Area",
                    "amenities": ["Playground", "Walking Trails"]
                }
            ]
        }
    }


@pytest.fixture
def temp_data_dir(sample_properties, sample_agents, sample_clients, sample_market_data, sample_amenities):
    """Create a temporary directory with test data files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create subdirectories
        os.makedirs(os.path.join(temp_dir, "properties"))
        os.makedirs(os.path.join(temp_dir, "agents"))
        os.makedirs(os.path.join(temp_dir, "clients"))
        os.makedirs(os.path.join(temp_dir, "market"))
        os.makedirs(os.path.join(temp_dir, "amenities"))
        os.makedirs(os.path.join(temp_dir, "transactions"))
        os.makedirs(os.path.join(temp_dir, "areas"))
        
        # Write test data files
        with open(os.path.join(temp_dir, "properties", "active_listings.json"), "w") as f:
            json.dump({"active_listings": sample_properties}, f)
        
        with open(os.path.join(temp_dir, "agents", "agent_profiles.json"), "w") as f:
            json.dump({"agents": sample_agents}, f)
        
        with open(os.path.join(temp_dir, "clients", "client_database.json"), "w") as f:
            json.dump({"clients": sample_clients}, f)
        
        with open(os.path.join(temp_dir, "market", "market_analytics.json"), "w") as f:
            json.dump(sample_market_data, f)
        
        with open(os.path.join(temp_dir, "amenities", "local_amenities.json"), "w") as f:
            json.dump(sample_amenities, f)
        
        # Create empty files for other data
        with open(os.path.join(temp_dir, "transactions", "recent_sales.json"), "w") as f:
            json.dump({"sales": []}, f)
        
        with open(os.path.join(temp_dir, "areas", "city_overview.json"), "w") as f:
            json.dump({"areas": []}, f)
        
        yield temp_dir


@pytest.fixture
def test_data_manager(temp_data_dir):
    """Create a RealEstateDataManager instance with test data"""
    return RealEstateDataManager(data_dir=temp_data_dir)


@pytest.fixture
def mock_mcp_server():
    """Create a mock FastMCP server for testing"""
    return Mock(spec=FastMCP)


@pytest.fixture
def property_filter():
    """Create a PropertyFilter instance for testing"""
    return PropertyFilter(
        min_price=400000,
        max_price=600000,
        min_bedrooms=2,
        areas=["Test Area"]
    ) 