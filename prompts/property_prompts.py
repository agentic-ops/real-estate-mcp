"""
Property-related prompt templates for the Real Estate MCP Server
"""

from mcp.server.fastmcp import FastMCP


def register_property_prompts(mcp: FastMCP):
    """Register all property-related prompt templates with the MCP server"""

    @mcp.prompt()
    def property_analysis_prompt(property_id: str = "PROP001") -> str:
        """
        Generate a comprehensive property analysis report

        This prompt creates a detailed analysis of a specific property including
        market context, features, investment potential, and pricing strategies.
        Useful for buyers, sellers, investors, and real estate agents.
        """
        return f"""
Please analyze property {property_id} and provide a comprehensive report including:

## 🏠 Property Analysis Report

### 1. Property Details and Features
- Physical characteristics and condition
- Unique selling points and standout features
- Recent improvements or renovations needed
- Property history and previous sales

### 2. Market Context and Comparable Sales
- Recent comparable sales in the area
- Price per square foot analysis
- Market positioning relative to similar properties
- Time on market trends for similar properties

### 3. Area Analysis and Neighborhood Intelligence
- Local amenities and convenience factors
- School districts and educational opportunities
- Transportation and commute accessibility
- Future development plans and area growth

### 4. Investment Potential Assessment
- Rental income potential and market rates
- Property appreciation trends and projections
- Cash flow analysis and ROI calculations
- Exit strategy considerations

### 5. Pricing Strategy Recommendations
- Optimal listing price range
- Market timing considerations
- Negotiation strategies and flexibility
- Marketing positioning recommendations

### 📊 Target Audience Insights:
- **Buyers**: Evaluation criteria and decision factors
- **Sellers**: Pricing optimization and market positioning
- **Investors**: Financial projections and risk assessment
- **Agents**: Marketing materials and client advisory

**Property ID to analyze: {property_id}**

Please use all available real estate tools to gather comprehensive data and provide actionable insights.
        """

    @mcp.prompt()
    def property_comparison_prompt(property_ids: str = "PROP001,PROP002") -> str:
        """
        Compare multiple properties side-by-side

        This prompt creates a detailed comparison of multiple properties to help
        with decision-making. Useful for buyers choosing between options or
        agents preparing comparative market analysis.
        """
        property_list = property_ids.split(",")
        property_list_formatted = ", ".join(property_list)

        return f"""
Please create a comprehensive comparison analysis for properties: {property_list_formatted}

## 🔍 Property Comparison Analysis

### 1. Side-by-Side Property Details
- Physical specifications and features comparison
- Condition and age assessment
- Unique characteristics of each property
- Pros and cons summary for each

### 2. Financial Comparison
- Purchase price and value analysis
- Cost per square foot comparison
- Estimated monthly costs (taxes, HOA, utilities)
- Financing considerations and requirements

### 3. Location and Area Comparison
- Neighborhood characteristics and amenities
- Commute times and transportation options
- School districts and ratings
- Future development impact

### 4. Investment Potential Comparison
- Rental income potential for each property
- Appreciation prospects and market trends
- Maintenance and improvement costs
- Resale potential and marketability

### 5. Recommendation Summary
- Best fit for different buyer profiles
- Risk assessment for each option
- Decision-making factors to consider
- Final recommendation with rationale

**Properties to compare: {property_list_formatted}**

Please provide a clear, data-driven comparison that helps with informed decision-making.
        """
