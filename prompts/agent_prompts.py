"""
Agent-related prompt templates for the Real Estate MCP Server
"""

from mcp.server.fastmcp import FastMCP


def register_agent_prompts(mcp: FastMCP):
    """Register all agent-related prompt templates with the MCP server"""

    def _generate_focus_area_strategy(focus_area):
        """Generate specific strategy content based on focus area"""
        strategies = {
            "lead_generation": """
#### Lead Generation Strategy Deep Dive:

##### Digital Lead Generation:
- **SEO Optimization**: Target local real estate keywords and location-based searches
- **PPC Campaigns**: Google Ads and Facebook Ads for property searches and market areas
- **Landing Pages**: Conversion-optimized pages for different buyer/seller segments
- **Lead Magnets**: Market reports, buyer guides, and property valuation tools
- **Retargeting**: Follow-up campaigns for website visitors and engaged prospects

##### Traditional Lead Generation:
- **Geographic Farming**: Consistent presence in target neighborhoods
- **Sphere of Influence**: Systematic outreach to personal and professional networks
- **Open Houses**: Strategic hosting and visitor capture systems
- **Referral Programs**: Incentivized referral systems for past clients and partners
- **Community Involvement**: Local events and organization participation

##### Lead Nurturing and Conversion:
- **CRM Integration**: Automated follow-up and lead scoring systems
- **Email Sequences**: Targeted nurturing campaigns by lead source and type
- **Value-Added Content**: Regular market updates and educational resources
- **Personal Outreach**: Phone calls and personal meetings for qualified leads
- **Conversion Tracking**: Monitor lead journey and optimize touchpoints
            """,
            "brand_building": """
#### Brand Building Strategy Deep Dive:

##### Brand Identity Development:
- **Value Proposition**: Clear differentiation and unique selling points
- **Brand Messaging**: Consistent communication across all channels
- **Visual Identity**: Professional photography, logos, and design elements
- **Brand Voice**: Tone and personality in all communications
- **Brand Standards**: Guidelines for consistent brand application

##### Brand Awareness Campaigns:
- **Content Marketing**: Thought leadership and market expertise demonstration
- **Social Media Presence**: Regular, valuable content sharing and engagement
- **Public Relations**: Media appearances and industry recognition
- **Community Involvement**: Local sponsorships and volunteer activities
- **Professional Networking**: Industry events and association participation

##### Brand Reputation Management:
- **Online Reviews**: Proactive review generation and management
- **Client Testimonials**: Systematic collection and promotion
- **Case Studies**: Success story documentation and sharing
- **Professional Awards**: Industry recognition and achievement promotion
- **Thought Leadership**: Market insights and trend analysis sharing
            """,
            "client_retention": """
#### Client Retention Strategy Deep Dive:

##### Post-Transaction Engagement:
- **Closing Follow-up**: Immediate post-closing satisfaction check
- **Quarterly Check-ins**: Regular communication and market updates
- **Anniversary Outreach**: Annual home purchase/sale anniversary contact
- **Holiday Greetings**: Seasonal cards and personal messages
- **Life Event Recognition**: Congratulations on promotions, births, etc.

##### Value-Added Services:
- **Market Updates**: Personalized property value and market reports
- **Home Maintenance**: Seasonal checklists and service provider referrals
- **Local Events**: Community event invitations and notifications
- **Educational Content**: Homeownership tips and real estate insights
- **Exclusive Access**: Preview opportunities and off-market listings

##### Referral Generation:
- **Referral Incentives**: Rewards for successful referrals
- **Referral Requests**: Strategic timing and approach for referral asks
- **Network Expansion**: Introduction to complementary service providers
- **Client Events**: Appreciation events and networking opportunities
- **Success Sharing**: Celebrate client achievements and milestones
            """,
        }

        return strategies.get(
            focus_area,
            "Strategy details will be customized based on the specific focus area.",
        )

    def _generate_skill_training_plan(skill_area):
        """Generate specific training content based on skill area"""
        training_plans = {
            "negotiation": """
#### Negotiation Skills Training Plan:

##### Core Negotiation Concepts:
- **Negotiation Theory**: Win-win vs. win-lose strategies
- **Communication Skills**: Active listening and persuasion techniques
- **Emotional Intelligence**: Reading people and managing emotions
- **Preparation Strategies**: Research and planning for negotiations
- **Closing Techniques**: Securing agreements and commitments

##### Real Estate Specific Applications:
- **Offer Negotiations**: Price, terms, and contingency discussions
- **Multiple Offer Situations**: Competitive bidding strategies
- **Inspection Negotiations**: Repair requests and credit discussions
- **Closing Issues**: Problem resolution and deal salvage
- **Commission Negotiations**: Fee discussions and value demonstration

##### Practice Scenarios:
- **Role-Playing Exercises**: Buyer and seller representation scenarios
- **Case Study Analysis**: Successful and challenging negotiation examples
- **Peer Practice Sessions**: Collaborative learning and feedback
- **Video Review**: Recording and analyzing negotiation interactions
- **Client Interaction Practice**: Real-world application with supervision
            """,
            "technology": """
#### Technology Skills Training Plan:

##### Digital Tools Mastery:
- **CRM Systems**: Contact management and lead tracking
- **MLS Platforms**: Property search and market analysis tools
- **Virtual Tour Technology**: 360-degree photography and video
- **Social Media Marketing**: Platform-specific strategies and tools
- **Email Marketing**: Automation and campaign management

##### Data Analysis and Reporting:
- **Market Analytics**: Comparative market analysis and trends
- **Performance Tracking**: KPI monitoring and reporting
- **Client Presentations**: Digital presentation tools and techniques
- **Mobile Applications**: On-the-go productivity and client service
- **Cloud Computing**: File sharing and remote collaboration

##### Implementation and Integration:
- **System Setup**: Configuration and customization
- **Workflow Optimization**: Process automation and efficiency
- **Training and Support**: Ongoing education and troubleshooting
- **Security and Privacy**: Data protection and compliance
- **ROI Measurement**: Technology investment evaluation
            """,
            "market_analysis": """
#### Market Analysis Skills Training Plan:

##### Market Research Fundamentals:
- **Data Collection**: Sources and reliability assessment
- **Statistical Analysis**: Trend identification and forecasting
- **Comparative Analysis**: Property and area comparisons
- **Economic Indicators**: Understanding market drivers
- **Seasonal Patterns**: Cyclical trends and timing factors

##### Analysis Tools and Techniques:
- **MLS Data Mining**: Advanced search and analysis techniques
- **Spreadsheet Modeling**: Financial and market calculations
- **Visualization Tools**: Charts, graphs, and presentation graphics
- **Report Writing**: Clear and compelling market reports
- **Client Presentation**: Effective communication of insights

##### Application and Practice:
- **CMA Preparation**: Comprehensive market analysis projects
- **Market Reports**: Regular area and trend analysis
- **Investment Analysis**: ROI and cash flow calculations
- **Client Education**: Market insight sharing and explanation
- **Competitive Intelligence**: Market positioning and strategy
            """,
        }

        return training_plans.get(
            skill_area,
            "Training plan details will be customized based on the specific skill area.",
        )

    @mcp.prompt()
    def agent_performance_prompt(agent_id: str = "AGT001") -> str:
        """
        Generate an agent performance dashboard and analysis

        This prompt creates comprehensive performance analysis for real estate agents
        including sales metrics, client relationships, market expertise, and
        recommendations for business development and improvement.
        """
        return f"""
Please create a comprehensive performance analysis for agent {agent_id}:

## 👤 Agent Performance Dashboard & Analysis

### 1. Agent Profile and Professional Overview
- Professional background and experience level
- Specialization areas and market expertise
- Certifications, designations, and continuing education
- Professional associations and industry involvement

### 2. Current Listings and Portfolio Analysis
- Active listing inventory and property types
- Listing quality and market positioning
- Pricing strategies and market competitiveness
- Marketing effectiveness and exposure metrics

### 3. Sales Performance and Key Metrics
- Year-to-date and historical sales volume
- Number of transactions and average sale price
- Days on market performance vs. market average
- Commission income and revenue trends

### 4. Client Base and Relationship Management
- Client acquisition and retention rates
- Referral generation and repeat business
- Client satisfaction scores and testimonials
- Database size and lead conversion rates

### 5. Market Area Coverage and Expertise
- Geographic specialization and market knowledge
- Area-specific performance and market share
- Competitive positioning within service areas
- Local market insights and trend awareness

### 6. Business Development and Growth Analysis
- Lead generation strategies and effectiveness
- Marketing and branding initiatives
- Technology adoption and digital presence
- Professional development and skill enhancement

### 📊 Performance Metrics Dashboard:

#### Sales Performance:
- **Total Sales Volume**: Year-to-date and annual figures
- **Transaction Count**: Number of closed deals
- **Average Sale Price**: Per transaction and trend analysis
- **Market Share**: Percentage of area market activity
- **Commission Income**: Revenue generation and growth

#### Efficiency Metrics:
- **Days on Market**: Average vs. market comparison
- **List-to-Sale Ratio**: Pricing accuracy and negotiation skills
- **Conversion Rate**: Leads to contracts percentage
- **Client Retention**: Repeat and referral business rate
- **Pipeline Health**: Pending and potential transactions

#### Market Expertise:
- **Area Knowledge**: Specialization depth and breadth
- **Market Trends**: Awareness and prediction accuracy
- **Competitive Analysis**: Positioning vs. other agents
- **Client Education**: Market insight sharing effectiveness
- **Professional Growth**: Skill development and adaptation

### 🎯 Performance Analysis by Category:

#### Strengths and Competitive Advantages:
- Top-performing areas and specializations
- Unique value propositions and differentiators
- Client relationship and service excellence
- Market knowledge and expertise areas

#### Improvement Opportunities:
- Performance gaps and development needs
- Market expansion and growth potential
- Skill enhancement and training opportunities
- Technology and process optimization

#### Strategic Recommendations:
- Business development priorities and actions
- Market positioning and branding strategies
- Client acquisition and retention improvements
- Professional development and education plans

### 💡 Success Benchmarking:

#### Industry Comparisons:
- Performance vs. local market averages
- Ranking within brokerage and market area
- Industry best practices and standards
- Peer group analysis and positioning

#### Growth Trajectory:
- Historical performance trends and patterns
- Future potential and growth projections
- Market opportunity assessment
- Career advancement and development path

### 🚀 Action Plan and Development Recommendations:

#### Immediate Actions (30-60 days):
- High-impact improvements and quick wins
- Client follow-up and relationship strengthening
- Marketing and lead generation optimization
- Process improvements and efficiency gains

#### Medium-term Goals (3-6 months):
- Skill development and training initiatives
- Market expansion and specialization development
- Technology adoption and digital enhancement
- Professional network and partnership building

#### Long-term Strategy (6-12 months):
- Business growth and market share expansion
- Brand development and market positioning
- Team building and support system development
- Career advancement and specialization mastery

**Agent ID: {agent_id}**

Please provide actionable insights for performance improvement, business development, and competitive positioning.
        """

    @mcp.prompt()
    def agent_marketing_strategy_prompt(
        agent_id: str = "AGT001", focus_area: str = "lead_generation"
    ) -> str:
        """
        Generate marketing and business development strategy for an agent

        This prompt creates comprehensive marketing strategies tailored to an agent's
        strengths, market position, and business development goals.
        """
        return f"""
Please develop a comprehensive marketing strategy for agent {agent_id} with focus on {focus_area}:

## 📈 Agent Marketing & Business Development Strategy

### 1. Current Market Position Assessment
- Brand awareness and market recognition
- Competitive landscape and positioning
- Unique value propositions and differentiators
- Target market and ideal client profile

### 2. Marketing Goals and Objectives
- Lead generation targets and conversion goals
- Brand building and awareness objectives
- Market share and growth aspirations
- Client retention and referral targets

### 3. Digital Marketing Strategy
- Website optimization and SEO enhancement
- Social media presence and content strategy
- Online advertising and PPC campaigns
- Email marketing and nurturing sequences

### 4. Traditional Marketing Approaches
- Print advertising and direct mail campaigns
- Networking events and community involvement
- Referral programs and partnership development
- Open houses and property marketing events

### 5. Content Marketing and Thought Leadership
- Market insights and trend analysis content
- Educational resources and buyer/seller guides
- Video marketing and virtual tour strategies
- Blog content and industry commentary

### 6. Client Relationship and Retention Strategies
- Client communication and follow-up systems
- Value-added services and client appreciation
- Referral incentives and loyalty programs
- Past client re-engagement and nurturing

### 🎯 Focus Area Deep Dive: {focus_area.replace('_', ' ').title()}

{_generate_focus_area_strategy(focus_area)}

### 📊 Marketing Channel Analysis:

#### Digital Channels:
- **Website & SEO**: Lead capture and conversion optimization
- **Social Media**: Platform-specific strategies and content plans
- **Email Marketing**: Segmentation and automation workflows
- **Online Advertising**: Targeted campaigns and budget allocation
- **Video Marketing**: Property showcases and market updates

#### Traditional Channels:
- **Networking**: Industry events and community involvement
- **Direct Mail**: Targeted campaigns and geographic farming
- **Print Advertising**: Strategic placement and brand building
- **Referral Programs**: Incentive structures and partner networks
- **Event Marketing**: Open houses and client appreciation events

### 💰 Budget Allocation and ROI Analysis:
- Marketing budget distribution by channel
- Cost per lead and acquisition metrics
- ROI tracking and performance measurement
- Budget optimization and reallocation strategies
- Investment priorities and resource allocation

### 📅 Implementation Timeline and Milestones:

#### Phase 1 (Month 1-2): Foundation Building
- Brand development and positioning
- Digital presence optimization
- Content creation and resource development
- System setup and process implementation

#### Phase 2 (Month 3-4): Campaign Launch
- Marketing campaign activation
- Lead generation system deployment
- Content distribution and promotion
- Performance tracking and optimization

#### Phase 3 (Month 5-6): Scale and Optimize
- Campaign performance analysis
- Strategy refinement and optimization
- Scale successful initiatives
- Expand successful channels and tactics

### 🎯 Success Metrics and KPIs:
- **Lead Generation**: Quantity, quality, and conversion rates
- **Brand Awareness**: Market recognition and recall metrics
- **Engagement**: Website traffic, social media, and content metrics
- **Conversion**: Lead-to-client and client-to-referral rates
- **ROI**: Marketing spend efficiency and revenue attribution

**Agent ID: {agent_id}**
**Focus Area: {focus_area.replace('_', ' ').title()}**

Please provide specific, actionable marketing strategies with clear implementation steps and success metrics.
        """

    @mcp.prompt()
    def agent_training_development_prompt(
        agent_id: str = "AGT001", skill_area: str = "negotiation"
    ) -> str:
        """
        Generate training and professional development plan for an agent

        This prompt creates comprehensive training recommendations and development
        plans to enhance agent skills and performance in specific areas.
        """
        return f"""
Please create a comprehensive training and development plan for agent {agent_id} focusing on {skill_area}:

## 🎓 Agent Training & Professional Development Plan

### 1. Current Skill Assessment
- Existing competency level and experience
- Strengths and areas for improvement
- Performance gaps and development needs
- Learning style and preferences assessment

### 2. Training Objectives and Goals
- Specific skill development targets
- Performance improvement benchmarks
- Timeline and milestone expectations
- Success metrics and evaluation criteria

### 3. Recommended Training Programs
- Industry certifications and designations
- Online courses and e-learning platforms
- Workshop and seminar opportunities
- Mentorship and coaching programs

### 4. Practical Application and Practice
- Role-playing scenarios and simulations
- Real-world application opportunities
- Peer learning and collaboration
- Case study analysis and discussion

### 5. Progress Tracking and Evaluation
- Skill assessment and progress monitoring
- Performance metrics and improvement tracking
- Feedback collection and analysis
- Continuous improvement and adjustment

### 🎯 Skill Focus: {skill_area.replace('_', ' ').title()}

{_generate_skill_training_plan(skill_area)}

### 📚 Recommended Learning Resources:

#### Formal Education:
- **Industry Certifications**: Relevant designations and credentials
- **Professional Courses**: Specialized training programs
- **University Programs**: Real estate and business education
- **Conference Attendance**: Industry events and networking
- **Continuing Education**: License maintenance and skill updates

#### Self-Directed Learning:
- **Books and Publications**: Industry literature and best practices
- **Podcasts and Videos**: Educational content and expert insights
- **Online Communities**: Professional forums and discussion groups
- **Webinars and Workshops**: Virtual learning opportunities
- **Industry Publications**: Trade magazines and research reports

### 💪 Skill Development Action Plan:

#### Phase 1 (Weeks 1-4): Foundation Building
- Initial skill assessment and gap analysis
- Core concept learning and theory foundation
- Basic technique practice and application
- Resource collection and study plan creation

#### Phase 2 (Weeks 5-8): Skill Development
- Advanced technique learning and practice
- Real-world application and experience
- Feedback collection and performance review
- Skill refinement and improvement focus

#### Phase 3 (Weeks 9-12): Mastery and Integration
- Advanced application and complex scenarios
- Teaching and mentoring others
- Performance evaluation and certification
- Continuous improvement and maintenance

### 📊 Progress Tracking and Metrics:
- **Skill Assessments**: Regular competency evaluations
- **Performance Metrics**: Quantifiable improvement measures
- **Client Feedback**: Service quality and satisfaction scores
- **Peer Reviews**: Colleague and supervisor evaluations
- **Self-Assessment**: Personal reflection and goal tracking

**Agent ID: {agent_id}**
**Skill Focus: {skill_area.replace('_', ' ').title()}**

Please provide specific, actionable training recommendations with clear development pathways and success metrics.
        """
