"""Mortgage and affordability MCP tools.

Deterministic, offline finance calculators built on
``tools.finance_helpers``. These provide payment estimates, amortization
schedules, affordability analysis, and refinance comparisons. They are
planning aids, not lending offers or financial advice.
"""

from __future__ import annotations

import json
from typing import Optional

from mcp.server.mcpserver import MCPServer

from tools.finance_helpers import (
    amortization_schedule,
    amortization_summary,
    estimate_affordability,
    monthly_mortgage_payment,
)
from utils import audit

DISCLAIMER = "Estimates for planning only. Not a lending offer or financial advice."


def register_mortgage_tools(mcp: MCPServer) -> None:
    """Register all mortgage/affordability tools with the MCP server."""

    @mcp.tool()
    def calculate_mortgage_payment(
        principal: float,
        annual_rate_pct: float,
        term_years: int = 30,
    ) -> str:
        """Calculate the monthly principal & interest payment for a loan.

        ``annual_rate_pct`` is a percentage (e.g. 6.5 for 6.5%).
        """
        audit(
            "calculate_mortgage_payment",
            principal=principal,
            annual_rate_pct=annual_rate_pct,
            term_years=term_years,
        )
        if term_years <= 0:
            return json.dumps({"error": "term_years must be positive."}, indent=2)
        summary = amortization_summary(principal, annual_rate_pct, term_years)
        summary["annual_rate_pct"] = annual_rate_pct
        summary["term_years"] = term_years
        summary["disclaimer"] = DISCLAIMER
        return json.dumps(summary, indent=2)

    @mcp.tool()
    def get_amortization_schedule(
        principal: float,
        annual_rate_pct: float,
        term_years: int = 30,
        max_rows: int = 12,
    ) -> str:
        """Return an amortization schedule (first ``max_rows`` months by default)."""
        audit(
            "get_amortization_schedule",
            principal=principal,
            term_years=term_years,
            max_rows=max_rows,
        )
        if term_years <= 0:
            return json.dumps({"error": "term_years must be positive."}, indent=2)
        rows = amortization_schedule(
            principal, annual_rate_pct, term_years, max_rows=max_rows
        )
        summary = amortization_summary(principal, annual_rate_pct, term_years)
        return json.dumps(
            {
                "summary": summary,
                "rows_returned": len(rows),
                "schedule": rows,
                "disclaimer": DISCLAIMER,
            },
            indent=2,
        )

    @mcp.tool()
    def estimate_affordability_tool(
        annual_income: float,
        monthly_debts: float = 0.0,
        down_payment: float = 0.0,
        annual_rate_pct: float = 6.5,
        term_years: int = 30,
        max_dti: float = 0.36,
    ) -> str:
        """Estimate the maximum affordable purchase price from income and DTI.

        Folds property tax and insurance into the monthly budget. Returns the
        supportable price, loan amount, and estimated monthly payment.
        """
        audit(
            "estimate_affordability",
            annual_income=annual_income,
            max_dti=max_dti,
        )
        result = estimate_affordability(
            annual_income=annual_income,
            monthly_debts=monthly_debts,
            down_payment=down_payment,
            annual_rate_pct=annual_rate_pct,
            term_years=term_years,
            max_dti=max_dti,
        )
        result["disclaimer"] = DISCLAIMER
        return json.dumps(result, indent=2)

    @mcp.tool()
    def compare_refinance(
        principal: float,
        current_rate_pct: float,
        new_rate_pct: float,
        term_years: int = 30,
        closing_costs: float = 0.0,
    ) -> str:
        """Compare a current loan to a refinance at a new rate.

        Returns the monthly savings and the break-even month once closing
        costs are recovered.
        """
        audit(
            "compare_refinance",
            current_rate_pct=current_rate_pct,
            new_rate_pct=new_rate_pct,
        )
        if term_years <= 0:
            return json.dumps({"error": "term_years must be positive."}, indent=2)
        current_payment = monthly_mortgage_payment(
            principal, current_rate_pct, term_years
        )
        new_payment = monthly_mortgage_payment(principal, new_rate_pct, term_years)
        monthly_savings = current_payment - new_payment
        break_even_month: Optional[int] = None
        if monthly_savings > 0:
            break_even_month = int(-(-closing_costs // monthly_savings)) or 1
        return json.dumps(
            {
                "principal": round(principal, 2),
                "term_years": term_years,
                "current_rate_pct": current_rate_pct,
                "new_rate_pct": new_rate_pct,
                "current_monthly_payment": round(current_payment, 2),
                "new_monthly_payment": round(new_payment, 2),
                "monthly_savings": round(monthly_savings, 2),
                "closing_costs": round(closing_costs, 2),
                "break_even_month": break_even_month,
                "recommendation": (
                    "Refinance likely beneficial if you keep the loan past the "
                    "break-even month."
                    if monthly_savings > 0
                    else "New rate does not lower the payment; refinance not indicated."
                ),
                "disclaimer": DISCLAIMER,
            },
            indent=2,
        )
