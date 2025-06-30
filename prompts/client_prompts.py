"""
Client-related prompt templates for the Real Estate MCP Server
"""

from mcp.server.fastmcp import FastMCP


def register_client_prompts(mcp: FastMCP):
    """Register all client-related prompt templates with the MCP server"""

    @mcp.prompt()
    def client_matching_prompt(client_id: str = "CLI001") -> str:
        """
        Generate personalized property recommendations for a client

        This prompt creates tailored property recommendations based on a client's
        profile, preferences, budget, and lifestyle requirements. Includes detailed
        analysis of why each property fits the client's criteria.
        """
        return f"""
Please create personalized property recommendations for client {client_id}:

## 🎯 Client Property Matching Report

### 1. Client Profile Analysis
- Current situation and motivation for buying/selling
- Budget constraints and financing pre-approval status
- Timeline and urgency factors
- Previous property search history and feedback

### 2. Preference Matching and Criteria Analysis
- Location preferences and must-have areas
- Property type and size requirements
- Feature priorities and deal-breakers
- Lifestyle factors and future planning

### 3. Curated Property Recommendations
- Top property matches with detailed explanations
- Why each property fits the client's criteria
- Potential concerns or compromises to discuss
- Viewing priority ranking and scheduling suggestions

### 4. Market Context and Strategy
- Current market conditions affecting the client
- Pricing trends in preferred areas
- Competition analysis and market timing
- Negotiation strategies and offer recommendations

### 5. Financial Analysis and Planning
- Budget alignment and financing options
- Total cost of ownership calculations
- Investment potential if applicable
- Risk factors and mitigation strategies

### 6. Next Steps and Action Plan
- Viewing schedule and property tour planning
- Documentation and preparation requirements
- Decision timeline and milestone planning
- Communication preferences and follow-up schedule

### 🏆 Success Factors:
- **Budget Alignment**: Properties within financial comfort zone
- **Location Fit**: Commute, amenities, and lifestyle compatibility  
- **Feature Match**: Must-have features and preferences satisfied
- **Market Timing**: Optimal timing for purchase decisions
- **Investment Value**: Long-term value and appreciation potential

**Client ID to analyze: {client_id}**

Please use client matching tools and property search capabilities to provide highly personalized recommendations.
        """

    @mcp.prompt()
    def client_consultation_prompt(
        client_id: str = "CLI001", consultation_type: str = "initial"
    ) -> str:
        """
        Generate a structured client consultation guide

        This prompt creates a comprehensive consultation framework for client meetings,
        covering needs assessment, market education, and service presentation.
        """
        return f"""
Please prepare a comprehensive consultation guide for client {client_id} ({consultation_type} consultation):

## 📋 Client Consultation Framework

### 1. Pre-Consultation Preparation
- Client background research and profile review
- Market data and area analysis preparation
- Comparable properties and market examples
- Documentation and presentation materials needed

### 2. Needs Assessment and Discovery
- Current living situation and motivation factors
- Budget parameters and financing readiness
- Timeline and urgency considerations
- Property preferences and non-negotiables

### 3. Market Education and Context
- Current market conditions and trends
- Area-specific insights and opportunities
- Pricing strategies and market positioning
- Competition analysis and market dynamics

### 4. Service Presentation and Value Proposition
- Agent expertise and specialization areas
- Service offerings and client support process
- Communication style and availability
- Success stories and client testimonials

### 5. Action Plan and Next Steps
- Property search strategy and criteria refinement
- Viewing schedule and market tour planning
- Documentation requirements and preparation
- Decision timeline and milestone tracking

### 6. Follow-up and Relationship Building
- Communication preferences and frequency
- Market updates and new listing alerts
- Check-in schedule and progress reviews
- Long-term relationship development

### 💡 Consultation Success Tips:
- **Listen Actively**: Understand underlying needs and concerns
- **Educate Thoroughly**: Provide market context and insights
- **Build Trust**: Demonstrate expertise and client focus
- **Plan Strategically**: Create clear action plans and timelines
- **Follow Through**: Consistent communication and service delivery

**Client ID: {client_id}**
**Consultation Type: {consultation_type}**

Please create a personalized consultation approach based on the client's profile and current market conditions.
        """

    @mcp.prompt()
    def client_feedback_analysis_prompt(client_id: str = "CLI001") -> str:
        """
        Analyze client feedback and refine search criteria

        This prompt helps analyze client feedback from property viewings and
        interactions to better understand preferences and refine the search strategy.
        """
        return f"""
Please analyze client feedback and refine the property search strategy for client {client_id}:

## 🔄 Client Feedback Analysis & Strategy Refinement

### 1. Feedback Pattern Analysis
- Property viewing feedback and reactions
- Consistent preferences and deal-breakers
- Evolving criteria and changing priorities
- Emotional responses and decision factors

### 2. Preference Refinement
- Updated must-have features and requirements
- Flexible criteria and potential compromises
- Location preferences and area expansion
- Budget adjustments and financial considerations

### 3. Search Strategy Optimization
- Refined search parameters and filters
- New areas or property types to consider
- Timing adjustments and market opportunities
- Viewing efficiency and scheduling improvements

### 4. Communication Enhancement
- Preferred communication style and frequency
- Information presentation and format preferences
- Decision-making process and timeline needs
- Support requirements and service expectations

### 5. Market Opportunity Identification
- Properties that match refined criteria
- Emerging opportunities and market changes
- Price adjustments and negotiation possibilities
- Off-market opportunities and pocket listings

### 6. Relationship Strengthening
- Trust-building opportunities and demonstrations
- Value-added services and market insights
- Long-term relationship development strategies
- Referral potential and network expansion

### 🎯 Optimization Goals:
- **Precision**: More accurate property matching
- **Efficiency**: Streamlined viewing and decision process
- **Satisfaction**: Enhanced client experience and outcomes
- **Success**: Faster path to successful property acquisition
- **Loyalty**: Long-term client relationship development

**Client ID: {client_id}**

Please provide actionable insights for improving client service and search effectiveness.
        """
