"""Integration tests for the mortgage/affordability tools."""

from tests.conftest import call_tool_json


class TestMortgageTools:
    async def test_calculate_mortgage_payment(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "calculate_mortgage_payment",
            {"principal": 400000, "annual_rate_pct": 6.5, "term_years": 30},
        )
        assert result["number_of_payments"] == 360
        assert result["monthly_payment"] > 0
        assert result["total_interest"] > 0
        assert "disclaimer" in result

    async def test_calculate_mortgage_invalid_term(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "calculate_mortgage_payment",
            {"principal": 400000, "annual_rate_pct": 6.5, "term_years": 0},
        )
        assert "error" in result

    async def test_amortization_schedule_truncated(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "get_amortization_schedule",
            {
                "principal": 250000,
                "annual_rate_pct": 5.0,
                "term_years": 30,
                "max_rows": 6,
            },
        )
        assert result["rows_returned"] == 6
        assert len(result["schedule"]) == 6
        assert result["summary"]["number_of_payments"] == 360

    async def test_estimate_affordability(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "estimate_affordability_tool",
            {"annual_income": 150000, "monthly_debts": 800, "down_payment": 50000},
        )
        assert result["max_purchase_price"] > result["down_payment"]
        assert "assumptions" in result

    async def test_compare_refinance_savings(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "compare_refinance",
            {
                "principal": 400000,
                "current_rate_pct": 7.0,
                "new_rate_pct": 5.5,
                "closing_costs": 6000,
            },
        )
        assert result["monthly_savings"] > 0
        assert result["break_even_month"] is not None

    async def test_compare_refinance_no_benefit(self, mcp_server):
        result = await call_tool_json(
            mcp_server,
            "compare_refinance",
            {"principal": 400000, "current_rate_pct": 5.0, "new_rate_pct": 6.0},
        )
        assert result["monthly_savings"] <= 0
        assert result["break_even_month"] is None
