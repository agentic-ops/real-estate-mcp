# Real Estate Data Portfolio

This folder contains mock data representing a real estate agent's portfolio and knowledge base.

## Current Implementation

The data is currently stored as static JSON files for demonstration purposes. This provides:
- Easy testing and development
- Consistent, predictable responses
- No external dependencies
- Complete offline functionality

## Modular Architecture

Each data source is designed as a modular component that can be replaced with:
- Independent API endpoints (MLS systems, market analytics platforms)
- Dedicated MCP servers (property search, market analysis, client management)
- AI agents (market trend analysis, client relationship management)
- Live database connections (CRM systems, property databases, market feeds)

This modular design allows swapping static data for live services without changing the core MCP server logic.

## Data Structure

### `/areas/`
- **`city_overview.json`** - City demographics, school districts, neighborhood profiles, and market trends

### `/properties/`
- **`active_listings.json`** - Property listings with specifications, pricing, and agent assignments

### `/agents/`
- **`agent_profiles.json`** - Agent profiles including specializations, experience, and achievements

### `/market/`
- **`market_analytics.json`** - Market data including trends, pricing analysis, and investment opportunities

### `/clients/`
- **`client_database.json`** - Client profiles with preferences, search history, and contact information

### `/amenities/`
- **`local_amenities.json`** - Local area information including schools, parks, shopping, and healthcare

### `/transactions/`
- **`recent_sales.json`** - Transaction history with sale details and market insights

## Usage

This data can be used to:
- Build real estate applications
- Test APIs and integrations
- Train AI systems
- Create analytics dashboards
- Develop MCP servers
- Demonstrate real estate domain knowledge 