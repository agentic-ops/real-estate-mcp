"""
Finance-oriented prompt templates for the Real Estate MCP Server

Covers mortgage/affordability planning and comparable-based valuation,
tying together the mortgage and valuation tool categories.
"""

from mcp.server.mcpserver import MCPServer


def register_finance_prompts(mcp: MCPServer):
    """Register mortgage and valuation prompt templates with the MCP server"""

    @mcp.prompt()
    def mortgage_planning_prompt(
        annual_income: str = "120000",
        down_payment: str = "60000",
    ) -> str:
        """
        Build a mortgage and affordability plan for a prospective buyer.

        Guides the assistant to use the mortgage tools (affordability,
        payment, amortization, refinance) to produce an actionable financing
        plan. Estimates only -- not a lending offer or financial advice.
        """
        return f"""
Please build a home-financing plan for a buyer with an annual income of
${annual_income} and ${down_payment} available for a down payment.

## 💰 Mortgage & Affordability Plan

### 1. Affordability
- Use `estimate_affordability_tool` to determine the maximum purchase price
  and supportable loan amount at current rates.
- State the assumed rate, term, and debt-to-income ratio.

### 2. Payment Breakdown
- Use `calculate_mortgage_payment` for the target loan to show principal &
  interest, total interest, and total paid over the term.
- Break out estimated property taxes and insurance.

### 3. Amortization Insight
- Use `get_amortization_schedule` to illustrate how principal vs. interest
  shifts over the first year and the loan life.

### 4. Rate Sensitivity & Refinance
- Compare payments at a few rate scenarios.
- Where relevant, use `compare_refinance` to show break-even timing.

### 5. Recommendation
- Summarize a realistic price range and monthly budget.
- Note key risks (rate changes, DTI headroom, reserves).

**Inputs: annual income ${annual_income}, down payment ${down_payment}**

Always label figures as planning estimates, not a lending offer.
        """

    @mcp.prompt()
    def valuation_prompt(property_id: str = "PROP001") -> str:
        """
        Produce a comparable-based valuation and investment read for a listing.

        Guides the assistant to combine valuation tools with market comps and
        investment metrics. Analytical estimate only -- not an appraisal.
        """
        return f"""
Please prepare a valuation and investment assessment for property
{property_id}.

## 🏷️ Valuation & Investment Assessment

### 1. Comparable-Based Value
- Use `estimate_property_value` to derive a CMA-style estimate and compare it
  to the list price.
- Use `comparable_market_analysis` for the property's area to ground the
  estimate in recent sales (avg price, price/sqft, days on market).

### 2. Pricing Read
- Is the listing under-, over-, or fairly priced versus comparables?
- What factors could justify a premium or discount?

### 3. Investment Metrics
- Use `analyze_listing_investment` with a reasonable market rent to compute
  cap rate, cash-on-cash return, and annual cash flow.
- Note sensitivity to rent, vacancy, and financing assumptions.

### 4. Recommendation
- Summarize value, pricing, and investment potential.
- Flag the biggest uncertainties and what data would reduce them.

**Property ID to value: {property_id}**

Label all figures as analytical estimates, not a certified appraisal.
        """
