# Real Estate MCP Server

A comprehensive Model Context Protocol (MCP) server for real estate data management. This server provides tools, resources, and prompts for property listings, agent management, market analysis, client relationships, and area intelligence.

## 🏗️ Architecture

The server is built with a modular, componentized architecture for maintainability and scalability:

```
real-estate-mcp/
├── main.py                    # Main server entry point
├── utils.py                   # Core data management utilities
├── tools/                     # MCP Tools (organized by category)
│   ├── property_tools.py      # Property search, filtering, insights
│   ├── agent_tools.py         # Agent profiles, performance, dashboards
│   ├── market_tools.py        # Market analysis and trends
│   ├── client_tools.py        # Client management and matching
│   ├── area_tools.py          # Area intelligence and amenities
│   └── system_tools.py        # Data management and system tools
├── resources/                 # MCP Resources (static and templates)
│   ├── static_resources.py    # Static data resources
│   └── resource_templates.py  # Dynamic resource templates
├── prompts/                   # MCP Prompts (user-controlled templates)
│   └── prompt_templates.py    # Analysis and reporting prompts
└── data/                      # Real estate data files
    ├── properties/
    ├── agents/
    ├── clients/
    ├── market/
    ├── transactions/
    ├── areas/
    └── amenities/
```

## 🚀 Features

### MCP Capabilities
- **30+ Tools**: Comprehensive real estate operations
- **10 Resources**: 5 static resources + 5 dynamic resource templates
- **5 Prompts**: User-controlled analysis templates
- **SSE Transport**: Web-compatible Server-Sent Events endpoint

### Tool Categories

#### 🏠 Property Management (7 tools)
- Search and filter properties by multiple criteria
- Get property details and comprehensive insights
- Area-based and agent-based property listings
- Market context and comparable analysis

#### 👥 Agent Operations (6 tools)
- Agent profiles and specializations
- Performance dashboards and metrics
- Client and property portfolio management
- Sales tracking and analytics

#### 📊 Market Analysis (7 tools)
- Market overview and price analytics
- Area-specific market performance
- Investment opportunity analysis
- Comparative area analysis
- Transaction tracking

#### 🤝 Client Management (3 tools)
- Client profiles and preferences
- Property matching algorithms
- Budget and criteria-based recommendations

#### 🏘️ Area Intelligence (9 tools)
- Comprehensive area reports
- Amenities and demographics
- Schools, parks, shopping, healthcare data
- City overview and area comparisons

#### ⚙️ System Management (2 tools)
- Data refresh and cache management
- System statistics and summaries

### Resources

#### Static Resources
- `realestate://all-properties`: Complete property listings
- `realestate://all-agents`: Agent directory
- `realestate://market-overview`: Current market trends
- `realestate://all-areas`: Area information
- `realestate://amenities`: Complete amenities database

#### Dynamic Resource Templates
- `realestate://properties/area/{area}`: Area-specific properties
- `realestate://agent/{agent_id}/dashboard`: Agent performance dashboard
- `realestate://market/area/{area}`: Area market analysis
- `realestate://property/{property_id}/insights`: Property insights
- `realestate://client/{client_id}/matches`: Client property matches

### Prompts
- **Property Analysis**: Comprehensive property evaluation
- **Client Matching**: Personalized recommendations
- **Market Reports**: Area market analysis
- **Agent Performance**: Performance dashboards
- **Investment Analysis**: ROI and opportunity assessment

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd real-estate-mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   python main.py
   ```

## 🔍 MCP Inspector

To inspect and debug your MCP server, you can use the MCP Inspector tool:

```bash
npx @modelcontextprotocol/inspector
```

This will launch the MCP Inspector interface, allowing you to:
- Monitor MCP messages in real-time
- Debug tool and resource calls
- Inspect server responses
- Test server functionality

## 🌐 Server Transport

The server uses **Server-Sent Events (SSE)** transport, making it compatible with:
- Web browsers and HTTP clients
- Traditional MCP clients
- Custom integrations

### Connection Details
- **SSE Endpoint**: `http://127.0.0.1:8000/sse` (for establishing SSE connection)
- **Message Endpoint**: `http://127.0.0.1:8000/messages/` (for posting MCP messages)
- **Transport**: SSE (Server-Sent Events)
- **Protocol**: MCP (Model Context Protocol)

### Web Client Example
```javascript
// Establish SSE connection
const eventSource = new EventSource('http://127.0.0.1:8000/sse');
eventSource.onmessage = function(event) {
    const mcpMessage = JSON.parse(event.data);
    // Handle MCP protocol messages
};

// Send MCP messages
async function sendMCPMessage(message) {
    const response = await fetch('http://127.0.0.1:8000/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(message)
    });
    return response.json();
}
```

## 🔧 Component Details

### Core Components

#### `utils.py` - Data Management
- `RealEstateDataManager`: Central data access class
- `PropertyFilter`: Search and filtering utilities
- JSON data loading and caching
- Cross-referencing and relationship mapping

#### `main.py` - Server Entry Point
- FastMCP server initialization
- Component registration orchestration
- SSE transport configuration
- Startup logging and diagnostics

### Tool Modules

Each tool module follows a consistent pattern:
```python
def register_[category]_tools(mcp: FastMCP):
    """Register all [category] tools with the MCP server"""
    
    @mcp.tool()
    def tool_function(parameters) -> str:
        """Tool description"""
        # Implementation
        return json.dumps(result, indent=2)
```

### Resource Modules

Resources provide direct access to data:
```python
@mcp.resource("resource-name")
def resource_function() -> str:
    """Resource description"""
    return json.dumps(data, indent=2)

@mcp.resource("template://path/{param}")
def template_function(param: str) -> str:
    """Template resource with parameters"""
    return json.dumps(filtered_data, indent=2)
```

### Prompt Templates

Prompts guide AI analysis:
```python
@mcp.prompt()
def analysis_prompt(param: str = "default") -> str:
    """Analysis prompt description"""
    return f"""
    Detailed analysis instructions for {param}...
    """
```

## 📊 Data Structure

The server operates on comprehensive real estate data:

- **5 Properties**: Victorian homes, contemporary, luxury, townhouses
- **3 Agents**: Specialized real estate professionals
- **6 Clients**: Buyers, sellers, investors with preferences
- **Multiple Sales**: Recent transaction history
- **5 Areas**: Downtown Riverside, Woodcrest, Canyon Crest, Arlington Heights, La Sierra
- **Amenities**: Schools, parks, shopping, healthcare facilities

## 🔍 Usage Examples

### MCP Client Examples

For proper MCP client integration, use the MCP protocol with the correct endpoints:

```bash
# Establish SSE connection (listen for server messages)
curl -N http://127.0.0.1:8000/sse

# Send MCP messages (in a separate terminal)
# Search properties
curl -X POST http://127.0.0.1:8000/messages/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_properties", "arguments": {"query": "Victorian"}}}'

# Filter by criteria
curl -X POST http://127.0.0.1:8000/messages/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "filter_properties", "arguments": {"min_price": 500000, "max_price": 1000000}}}'

# Get market overview
curl -X POST http://127.0.0.1:8000/messages/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": "realestate://market-overview"}}'

# Match client preferences
curl -X POST http://127.0.0.1:8000/messages/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "match_client_preferences", "arguments": {"client_id": "CLI001"}}}'
```

## 🛠️ Development

### Adding New Tools
1. Choose appropriate category in `tools/`
2. Add tool function with `@mcp.tool()` decorator
3. Register in the category's `register_*_tools()` function
4. Import and call registration in `main.py`

### Adding New Resources
1. Add to `resources/static_resources.py` for static data
2. Add to `resources/resource_templates.py` for parameterized resources
3. Use `@mcp.resource()` decorator with URI pattern

### Adding New Prompts
1. Add to `prompts/prompt_templates.py`
2. Use `@mcp.prompt()` decorator
3. Include parameter defaults and comprehensive instructions

## 🔄 Benefits of SSE Transport

- **Web Compatible**: Direct browser integration
- **Real-time**: Server-sent events for live updates
- **HTTP Standard**: Works with standard HTTP tools
- **Firewall Friendly**: Uses standard HTTP port
- **Scalable**: Supports multiple concurrent connections

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your component following the established patterns
4. Test thoroughly
5. Submit a pull request

---

## 📖 Further Reading

For a comprehensive deep dive into the architecture, design principles, and real-world applications of this MCP server, read the detailed blog post:

**[🔌 MCP Servers - Model Context Protocol Implementation](https://edwin.genego.io/ai/mcp-servers)**

The blog post covers:
- Understanding MCP Servers and their business impact
- Architecture deep dive with code examples
- MCP Tools, Prompts, and Resources explained
- Real-world usage scenarios and implementation patterns
- Security considerations and best practices
- Future implications of MCP technology

---

*Built with the Model Context Protocol (MCP) for seamless AI integration* 