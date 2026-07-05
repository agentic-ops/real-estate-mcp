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

### `config_resources.py`
Always-on server configuration (registered regardless of feature flags):
- `realestate://server-config` - Enabled tool categories, their environment
  variable names, and data statistics

### `integration_resources.py`
Optional live-integration status (registered when the `integrations` category
is enabled):
- `realestate://integrations/status` - Enabled/configured state for the
  Census, Walk Score, FEMA, FRED, FBI Crime Data, EPA, NOAA (free), and
  RentCast, Zillow (paid) adapters (never returns API keys)

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

Resources are registered when the MCP server starts. The package exposes a
single entry point, `register_all_resources(mcp)`, which registers the
always-on config resource plus every enabled domain's resources (gated by the
same `REALESTATE_MCP_ENABLE_*` feature flags as the tools):

```python
from resources import register_all_resources

register_all_resources(mcp)
```

Individual `register_*_resources(mcp)` functions remain available for
fine-grained use.

## Resource URI Patterns

- **Static Resources**: `realestate://resource-name`
- **Parameterized Resources**: `realestate://resource-name/{parameter}`
- **Nested Resources**: `realestate://entity/{id}/sub-resource` 