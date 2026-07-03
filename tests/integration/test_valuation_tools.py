"""Integration tests for the valuation and investment tools."""

from tests.conftest import call_tool_json


class TestValuationTools:
    async def test_estimate_property_value_real_listing(self, mcp_server):
        # PROP001 ships in the seed data.
        result = await call_tool_json(
            mcp_server, "estimate_property_value", {"property_id": "PROP001"}
        )
        assert result["property_id"] == "PROP001"
        assert "estimated_value" in result
        assert "assessment" in result

    async def test_estimate_property_value_missing(self, mcp_server):
        result = await call_tool_json(
            mcp_server, "estimate_property_value", {"property_id": "NOPE"}
        )
        assert "error" in result

    async def test_comparable_market_analysis(self, mcp_server):
        # Use an area that exists in the seed sales data.
        result = await call_tool_json(
            mcp_server,
            "comparable_market_analysis",
            {"area": "Downtown Riverside"},
        )
        assert "comparable_count" in result

    async def test_analyze_investment(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "analyze_investment",
            {"price": 500000, "monthly_rent": 3000, "down_payment": 100000},
        )
        assert result["cap_rate_pct"] is not None
        assert result["loan_amount"] == 400000
        assert "cash_on_cash_return_pct" in result

    async def test_analyze_investment_invalid_price(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "analyze_investment",
            {"price": 0, "monthly_rent": 3000, "down_payment": 0},
        )
        assert "error" in result

    async def test_analyze_listing_investment(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "analyze_listing_investment",
            {"property_id": "PROP001", "monthly_rent": 2800, "down_payment_pct": 20},
        )
        assert result["property_id"] == "PROP001"
        assert result["down_payment_pct"] == 20
        assert result["loan_amount"] > 0

    async def test_analyze_listing_investment_missing(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "analyze_listing_investment",
            {"property_id": "NOPE", "monthly_rent": 2800},
        )
        assert "error" in result
