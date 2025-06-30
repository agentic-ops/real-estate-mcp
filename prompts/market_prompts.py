"""
Market and investment-related prompt templates for the Real Estate MCP Server
"""

from mcp.server.fastmcp import FastMCP


def _generate_comparison_matrix(areas):
    """Generate a comparison matrix template for the areas"""
    matrix = "\n"
    for area in areas:
        area = area.strip()
        matrix += f"""
#### {area}:
- **Median Price**: [Price analysis]
- **Market Velocity**: [Days on market / absorption rate]
- **Inventory Level**: [Months of supply]
- **Demographics**: [Key population characteristics]
- **Amenities Score**: [Quality of life rating]
- **Growth Potential**: [Future development prospects]
- **Investment Grade**: [Investor suitability rating]
"""
    return matrix


def register_market_prompts(mcp: FastMCP):
    """Register all market and investment-related prompt templates with the MCP server"""

    @mcp.prompt()
    def market_report_prompt(area: str = "Downtown Riverside") -> str:
        """
        Generate a comprehensive market report for an area

        This prompt creates detailed market analysis including trends, pricing,
        inventory, demographics, and future predictions for a specific area.
        Valuable for buyers, sellers, investors, and agents.
        """
        return f"""
Please create a comprehensive market report for {area}:

## 📊 Market Analysis Report: {area}

### 1. Current Market Overview and Trends
- Market status (buyer's/seller's/balanced market)
- Recent market shifts and momentum indicators
- Seasonal patterns and cyclical trends
- Economic factors affecting the local market

### 2. Price Analysis and Historical Performance
- Current median home prices and price ranges
- Year-over-year price appreciation trends
- Price per square foot analysis by property type
- Historical price performance over 1, 3, and 5 years

### 3. Active Listings and Inventory Analysis
- Current inventory levels and months of supply
- New listings vs. pending sales ratio
- Days on market trends and absorption rates
- Price reduction patterns and market velocity

### 4. Recent Sales and Transaction Analysis
- Recent comparable sales and transaction volume
- Sale price vs. list price ratios
- Time to contract and closing statistics
- Cash vs. financed purchase patterns

### 5. Area Demographics and Lifestyle Factors
- Population demographics and growth trends
- Income levels and employment statistics
- School districts and educational quality
- Local amenities and quality of life factors

### 6. Future Market Predictions and Opportunities
- Development projects and infrastructure improvements
- Population growth projections and demand drivers
- Market outlook and investment opportunities
- Risk factors and potential challenges

### 🎯 Stakeholder Insights:

#### For Buyers:
- Best opportunities and optimal timing strategies
- Negotiation leverage and market positioning
- Emerging areas and value opportunities
- Financing considerations and market risks

#### For Sellers:
- Optimal pricing strategies and market positioning
- Timing recommendations and seasonal factors
- Property improvements and staging suggestions
- Marketing strategies and competitive advantages

#### For Investors:
- ROI potential and cash flow analysis
- Rental market demand and yield projections
- Appreciation prospects and market cycles
- Risk assessment and portfolio diversification

#### For Agents:
- Market positioning and client advisory strategies
- Lead generation opportunities and market niches
- Competitive landscape and differentiation
- Client education and market communication

### 📈 Key Performance Indicators:
- **Market Velocity**: Days on market and absorption rates
- **Price Trends**: Appreciation rates and price stability
- **Supply/Demand**: Inventory levels and buyer competition
- **Economic Health**: Employment, income, and growth indicators
- **Future Potential**: Development and infrastructure investments

**Area to analyze: {area}**

Please provide actionable, data-driven insights that support informed real estate decisions.
        """

    @mcp.prompt()
    def investment_analysis_prompt(
        budget_min: str = "500000", budget_max: str = "1000000"
    ) -> str:
        """
        Generate investment opportunity analysis within a budget range

        This prompt creates comprehensive investment analysis including ROI calculations,
        market opportunities, risk assessment, and strategic recommendations for
        real estate investors within a specific budget range.
        """
        return f"""
Please analyze investment opportunities in the ${budget_min} - ${budget_max} range:

## 💰 Real Estate Investment Analysis Report

### 1. Market Overview and Investment Climate
- Current investment market conditions
- Interest rates and financing environment
- Economic indicators affecting real estate investment
- Market cycle positioning and timing considerations

### 2. Property Opportunities by Area and Type
- Investment-grade properties within budget range
- Area-specific opportunities and market dynamics
- Property types with best investment potential
- Emerging markets and value-add opportunities

### 3. Rental Market Analysis and Yield Potential
- Current rental rates by area and property type
- Rental demand trends and tenant demographics
- Vacancy rates and market saturation analysis
- Rental yield calculations and cash flow projections

### 4. Financial Analysis and ROI Projections
- Purchase price analysis and negotiation opportunities
- Financing options and leverage strategies
- Cash flow projections and break-even analysis
- Total return calculations (cash flow + appreciation)

### 5. Risk Assessment and Market Factors
- Market risk factors and mitigation strategies
- Property-specific risks and due diligence requirements
- Economic sensitivity and market volatility
- Diversification considerations and portfolio balance

### 6. Investment Strategy Recommendations
- Optimal investment approach for budget range
- Timing strategies and market entry points
- Property management and operational considerations
- Exit strategy planning and timeline optimization

### 🏆 Investment Opportunity Categories:

#### Cash Flow Properties
- Properties generating positive monthly cash flow
- Stable rental markets with consistent demand
- Lower maintenance and management requirements
- Suitable for passive income generation

#### Value-Add Opportunities
- Properties requiring improvements or repositioning
- Below-market purchase prices with upside potential
- Renovation and improvement cost analysis
- Enhanced rental rates and appreciation potential

#### Appreciation Plays
- Properties in high-growth areas with development
- Long-term appreciation potential over cash flow
- Market timing and cycle positioning strategies
- Higher risk/reward investment profiles

#### Diversification Options
- Geographic diversification opportunities
- Property type diversification strategies
- Risk distribution and portfolio balance
- Market correlation and independence factors

### 📊 Financial Projections and Metrics:

#### Key Investment Metrics:
- **Cap Rate**: Net operating income / purchase price
- **Cash-on-Cash Return**: Annual cash flow / initial investment
- **IRR**: Internal rate of return over investment period
- **DSCR**: Debt service coverage ratio for financing
- **ROI**: Total return on investment including appreciation

#### Cost Analysis:
- **Acquisition Costs**: Purchase price, closing costs, inspections
- **Improvement Costs**: Renovations, repairs, and upgrades
- **Operating Expenses**: Property taxes, insurance, maintenance
- **Financing Costs**: Interest rates, points, and loan fees
- **Management Costs**: Property management and vacancy allowances

### 🎯 Investment Success Factors:
- **Location Quality**: Desirable areas with growth potential
- **Property Condition**: Well-maintained with minimal deferred maintenance
- **Market Timing**: Favorable purchase timing and market conditions
- **Financing Strategy**: Optimal leverage and interest rate environment
- **Management Plan**: Effective property management and tenant relations

**Budget Range: ${budget_min} - ${budget_max}**

Please focus on data-driven investment recommendations with clear financial projections and risk assessments.
        """

    @mcp.prompt()
    def comparative_market_analysis_prompt(
        areas: str = "Downtown Riverside,Woodcrest",
    ) -> str:
        """
        Generate comparative analysis between multiple market areas

        This prompt creates side-by-side market comparison for multiple areas,
        helping identify the best opportunities and investment potential across
        different neighborhoods or regions.
        """
        area_list = areas.split(",")
        area_list_formatted = ", ".join([area.strip() for area in area_list])

        return f"""
Please create a comprehensive comparative market analysis for: {area_list_formatted}

## 🔍 Comparative Market Analysis Report

### 1. Market Overview Comparison
- Current market conditions in each area
- Market velocity and transaction volume
- Buyer demand and seller motivation levels
- Market maturity and development stage

### 2. Price Analysis and Affordability
- Median home prices and price ranges by area
- Price per square foot comparisons
- Affordability indexes and income requirements
- Price appreciation trends and stability

### 3. Property Inventory and Selection
- Available inventory levels and variety
- Property types and architectural styles
- New construction vs. existing home options
- Luxury vs. starter home market segments

### 4. Demographics and Lifestyle Factors
- Population characteristics and growth trends
- Age demographics and household compositions
- Income levels and employment centers
- Educational attainment and school quality

### 5. Amenities and Quality of Life
- Shopping, dining, and entertainment options
- Parks, recreation, and outdoor activities
- Healthcare facilities and services
- Transportation and commute accessibility

### 6. Investment and Growth Potential
- Development projects and infrastructure improvements
- Economic development and job growth
- Population growth projections and demand drivers
- Long-term appreciation potential and market outlook

### 📊 Area-by-Area Comparison Matrix:

{_generate_comparison_matrix(area_list)}

### 🎯 Best Fit Analysis:

#### For First-Time Buyers:
- Most affordable areas with good value
- Areas with starter home inventory
- Neighborhoods with growth potential
- Communities with good schools and amenities

#### For Families:
- Areas with top-rated schools
- Family-friendly neighborhoods and amenities
- Safe communities with low crime rates
- Areas with parks and recreational facilities

#### For Professionals:
- Areas with easy commute access
- Neighborhoods with urban amenities
- Areas with networking and social opportunities
- Communities with modern housing options

#### For Investors:
- Areas with strong rental demand
- Neighborhoods with appreciation potential
- Markets with positive cash flow opportunities
- Areas with development and growth catalysts

#### For Retirees:
- Areas with healthcare access
- Quiet, safe neighborhoods
- Communities with senior-friendly amenities
- Areas with lower cost of living

### 💡 Strategic Recommendations:
- **Best Overall Value**: Area offering optimal price/quality balance
- **Highest Growth Potential**: Area with strongest future prospects
- **Best Rental Market**: Area with strongest investor opportunities
- **Most Affordable**: Area with best entry-level opportunities
- **Premium Choice**: Area with highest quality of life factors

**Areas Analyzed: {area_list_formatted}**

Please provide clear, data-driven comparisons that help with informed area selection decisions.
        """
