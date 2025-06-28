"""
Prompt templates for the Real Estate MCP Server
"""

from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP):
    """Register all prompt templates with the MCP server"""
    
    @mcp.prompt()
    def property_analysis_prompt(property_id: str = "PROP001") -> str:
        """Generate a comprehensive property analysis report"""
        return f"""
        Please analyze property {property_id} and provide a comprehensive report including:
        
        1. Property Details and Features
        2. Market Context and Comparable Sales
        3. Area Analysis and Amenities
        4. Investment Potential
        5. Pricing Strategy Recommendations
        
        Use the available tools to gather all necessary data and provide insights that would be valuable for:
        - Potential buyers evaluating the property
        - Sellers considering pricing strategies
        - Investors assessing rental or resale potential
        - Real estate agents preparing marketing materials
        
        Property ID to analyze: {property_id}
        """

    @mcp.prompt()
    def client_matching_prompt(client_id: str = "CLI001") -> str:
        """Generate personalized property recommendations for a client"""
        return f"""
        Please create personalized property recommendations for client {client_id}:
        
        1. Analyze the client's profile, preferences, and budget
        2. Find matching properties using the client matching tools
        3. Provide detailed analysis of each recommended property
        4. Explain why each property fits the client's criteria
        5. Include market insights and area information
        6. Suggest viewing priorities and negotiation strategies
        
        Consider factors like:
        - Budget alignment and financing options
        - Location preferences and commute considerations
        - Property features and lifestyle fit
        - Market timing and pricing trends
        - Investment potential if applicable
        
        Client ID to analyze: {client_id}
        """

    @mcp.prompt()
    def market_report_prompt(area: str = "Downtown Riverside") -> str:
        """Generate a comprehensive market report for an area"""
        return f"""
        Please create a comprehensive market report for {area}:
        
        1. Current Market Overview and Trends
        2. Price Analysis and Historical Performance
        3. Active Listings and Inventory Analysis
        4. Recent Sales and Transaction Analysis
        5. Area Demographics and Amenities
        6. Future Market Predictions and Opportunities
        
        Include insights for:
        - Buyers: Best opportunities and timing
        - Sellers: Pricing strategies and market positioning
        - Investors: ROI potential and rental market analysis
        - Agents: Market positioning and client advisory
        
        Focus on actionable insights and data-driven recommendations.
        
        Area to analyze: {area}
        """

    @mcp.prompt()
    def agent_performance_prompt(agent_id: str = "AGT001") -> str:
        """Generate an agent performance dashboard and analysis"""
        return f"""
        Please create a comprehensive performance analysis for agent {agent_id}:
        
        1. Agent Profile and Specializations
        2. Current Listings and Portfolio Analysis
        3. Recent Sales Performance and Metrics
        4. Client Base and Relationship Management
        5. Market Area Coverage and Expertise
        6. Performance Benchmarking and Recommendations
        
        Analyze:
        - Sales volume and transaction velocity
        - Average days on market for listings
        - Client satisfaction and retention
        - Market area expertise and coverage
        - Competitive positioning
        - Growth opportunities and recommendations
        
        Provide actionable insights for performance improvement and business development.
        
        Agent ID to analyze: {agent_id}
        """

    @mcp.prompt()
    def investment_analysis_prompt(budget_min: str = "500000", budget_max: str = "1000000") -> str:
        """Generate investment opportunity analysis within a budget range"""
        return f"""
        Please analyze investment opportunities in the ${budget_min} - ${budget_max} range:
        
        1. Market Overview and Investment Climate
        2. Property Opportunities by Area and Type
        3. Rental Market Analysis and Yield Potential
        4. Cash Flow Projections and ROI Analysis
        5. Risk Assessment and Market Factors
        6. Investment Strategy Recommendations
        
        Consider:
        - Purchase price vs. rental income potential
        - Area growth prospects and development plans
        - Property appreciation trends
        - Maintenance and management considerations
        - Exit strategy options
        - Market timing and financing conditions
        
        Focus on data-driven investment recommendations with clear financial projections.
        
        Budget range: ${budget_min} - ${budget_max}
        """ 