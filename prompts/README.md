# Real Estate MCP Prompts

This folder contains prompt templates for the Real Estate MCP Server. Prompts in the Model Context Protocol (MCP) are reusable templates that clients can use to interact with the server in standardized ways.

## What are MCP Prompts?

MCP prompts are predefined templates that:
- Accept dynamic arguments to customize behavior
- Include context from resources and tools
- Guide specific workflows and interactions
- Surface as UI elements in MCP clients (like slash commands)
- Provide standardized ways to interact with the server

Prompts are **user-controlled**, meaning they are exposed to clients for users to explicitly select and use. They enable consistent, reusable interactions with the real estate data and tools.

## Tools vs Prompts

Understanding the difference between MCP tools and prompts:

### Tools
- **What**: Functions that perform actions or retrieve data
- **Purpose**: Execute specific operations (search properties, get market data, etc.)
- **Usage**: Called by LLMs/agents to perform concrete tasks
- **Examples**: `search_properties()`, `get_market_analytics()`, `find_clients()`

### Prompts  
- **What**: Templates that structure conversations and workflows
- **Purpose**: Provide reusable workflows and guide interactions
- **Usage**: Can be invoked by users directly or discovered/used by AI agents
- **Examples**: Property analysis workflow, client consultation guide

**Key difference**: Tools perform specific functions, while prompts provide structured templates. Both can be used by users or AI agents, but prompts are designed to be exposed as actionable workflows in client UIs.

**In practice**: An agent might discover and use a prompt (like "analyze this property"), which provides a structured template that then guides the agent to use various tools (property search, market data, comparable sales) to complete the analysis.

## Available Prompt Categories

### Property Prompts (`property_prompts.py`)
Property analysis and comparison workflows:
- **`property_analysis_prompt`** - Comprehensive property analysis including market context, features, investment potential, and pricing strategies
- **`property_comparison_prompt`** - Side-by-side comparison of multiple properties for decision-making

### Client Prompts (`client_prompts.py`)
Client matching and consultation workflows:
- Client preference analysis and matching
- Consultation preparation and guidance
- Buyer/seller advisory prompts

### Market Prompts (`market_prompts.py`)
Market analysis and investment opportunity workflows:
- Market trend analysis and reporting
- Investment opportunity identification
- Comparative market analysis (CMA) generation

### Agent Prompts (`agent_prompts.py`)
Agent performance and business development workflows:
- Agent performance analysis and reporting
- Business development strategies
- Client relationship management guidance

## How Prompts Work

1. **Discovery**: Clients discover available prompts via `prompts/list` requests
2. **Execution**: Clients execute prompts via `prompts/get` requests with arguments
3. **Response**: Server returns formatted messages ready for LLM consumption
4. **Integration**: Prompts can surface as slash commands, quick actions, or guided workflows in client UIs

## Prompt Structure

Each prompt is implemented as a Python function with:
- `@mcp.prompt()` decorator for registration
- Clear docstring describing purpose and usage
- Optional parameters with default values
- Formatted prompt template as return value

Example:
```python
@mcp.prompt()
def property_analysis_prompt(property_id: str = "PROP001") -> str:
    """Generate a comprehensive property analysis report"""
    return f"Please analyze property {property_id}..."
```

## Usage in MCP Clients

These prompts will appear in MCP-compatible clients as:
- Slash commands (e.g., `/property-analysis`)
- Quick action buttons
- Guided workflow templates
- Context menu options

## Registration

All prompts are automatically registered with the MCP server through the `register_all_prompts()` function in `__init__.py`, which imports and registers prompts from all categories.

## Integration with Real Estate Tools

Prompts are designed to work seamlessly with the real estate tools and data sources, automatically leveraging:
- Property listings and details
- Market analytics and trends
- Client preferences and history
- Agent profiles and performance data
- Local amenities and area information

For more information about MCP prompts, see the [official documentation](https://modelcontextprotocol.io/docs/concepts/prompts). 