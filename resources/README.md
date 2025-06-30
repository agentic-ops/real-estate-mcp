# Real Estate MCP Resources

This folder contains resource definitions for the Real Estate MCP Server. Resources provide structured data access through URI-based endpoints.

## Current Implementation

Resources are currently implemented as Python functions that return JSON data from static data sources. Each resource is registered with the MCP server and accessible via specific URIs.

## Modular Architecture

Each resource module is designed as an independent component that can be:
- Replaced with live API integrations
- Connected to external databases
- Enhanced with AI-powered data processing
- Scaled independently based on usage patterns

## Resource Modules

### `property_resources.py`
Property-related data access:
- `realestate://all-properties` - Complete property listings
- `realestate://properties/area/{area}` - Properties filtered by area
- `realestate://property/{property_id}/insights` - Detailed property analysis

### `agent_resources.py`
Agent-related data access:
- `realestate://all-agents` - Complete agent directory
- `realestate://agent/{agent_id}/dashboard` - Agent performance metrics and listings

### `market_resources.py`
Market analysis and trends:
- `realestate://market-overview` - General market overview
- `realestate://market/area/{area}` - Area-specific market analysis

### `client_resources.py`
Client relationship management:
- `realestate://client/{client_id}/matches` - Properties matching client preferences

### `location_resources.py`
Geographic and amenity information:
- `realestate://all-areas` - City area information
- `realestate://amenities` - Local amenities and services

## Usage

Resources are automatically registered when the MCP server starts. Each module exports a registration function that adds its resources to the server:

```python
from resources import (
    register_property_resources,
    register_agent_resources,
    register_market_resources,
    register_client_resources,
    register_location_resources
)

# Register all resources with the MCP server
register_property_resources(mcp)
register_agent_resources(mcp)
register_market_resources(mcp)
register_client_resources(mcp)
register_location_resources(mcp)
```

## Resource URI Patterns

- **Static Resources**: `realestate://resource-name`
- **Parameterized Resources**: `realestate://resource-name/{parameter}`
- **Nested Resources**: `realestate://entity/{id}/sub-resource` 