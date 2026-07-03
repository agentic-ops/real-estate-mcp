"""Property valuation and investment-analysis MCP tools.

Comparable-based (CMA-style) valuation and buy-and-hold investment metrics.
Valuation uses the local comparable-sales data; investment math is provided
by ``tools.finance_helpers``. These are analytical estimates, not appraisals.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from tools.finance_helpers import investment_metrics
from utils import audit, get_data_manager

DISCLAIMER = "Analytical estimate only. Not a certified appraisal or financial advice."


def _price_per_sqft(record: Dict[str, Any]) -> Optional[float]:
    """Best-effort price-per-square-foot for a sale or listing record."""

    explicit = record.get("price_per_sqft")
    if isinstance(explicit, (int, float)) and explicit > 0:
        return float(explicit)
    price = record.get("sale_price") or record.get("price")
    sqft = record.get("square_feet")
    if price and sqft:
        return round(price / sqft, 2)
    return None


def _area_ppsf(sales: List[Dict[str, Any]]) -> Optional[float]:
    values = [v for v in (_price_per_sqft(s) for s in sales) if v]
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def register_valuation_tools(mcp: FastMCP) -> None:
    """Register valuation and investment tools with the MCP server."""

    data = get_data_manager()

    @mcp.tool()
    def estimate_property_value(property_id: str) -> str:
        """Estimate a property's value from comparable area sales (CMA-style).

        Multiplies the property's square footage by the average price-per-
        square-foot of recent sales in its area, and compares the estimate to
        the current list price.
        """
        audit("estimate_property_value", property_id=property_id)
        prop = data.get_property_by_id(property_id)
        if not prop:
            return json.dumps(
                {"error": f"Property with ID {property_id} not found"}, indent=2
            )
        area = prop.get("area", "")
        comps = data.get_sales_by_area(area)
        area_ppsf = _area_ppsf(comps)
        sqft = prop.get("square_feet")
        list_price = prop.get("price")
        estimated_value: Optional[float] = None
        if area_ppsf and sqft:
            estimated_value = round(area_ppsf * sqft, 2)
        delta_pct: Optional[float] = None
        if estimated_value and list_price:
            delta_pct = round(
                ((list_price - estimated_value) / estimated_value) * 100.0, 2
            )
        return json.dumps(
            {
                "property_id": property_id,
                "area": area,
                "square_feet": sqft,
                "list_price": list_price,
                "comparable_count": len(comps),
                "area_avg_price_per_sqft": area_ppsf,
                "estimated_value": estimated_value,
                "list_vs_estimate_pct": delta_pct,
                "assessment": _assessment(delta_pct),
                "disclaimer": DISCLAIMER,
            },
            indent=2,
        )

    @mcp.tool()
    def comparable_market_analysis(area: str) -> str:
        """Summarize comparable sales for an area (avg price, price/sqft, DOM)."""
        audit("comparable_market_analysis", area=area)
        comps = data.get_sales_by_area(area)
        if not comps:
            return json.dumps(
                {
                    "area": area,
                    "comparable_count": 0,
                    "message": "No comparable sales.",
                },
                indent=2,
            )
        prices = [c.get("sale_price", 0) for c in comps if c.get("sale_price")]
        doms = [c.get("days_on_market", 0) for c in comps if "days_on_market" in c]
        return json.dumps(
            {
                "area": area,
                "comparable_count": len(comps),
                "average_sale_price": (
                    round(sum(prices) / len(prices), 2) if prices else None
                ),
                "min_sale_price": min(prices) if prices else None,
                "max_sale_price": max(prices) if prices else None,
                "average_price_per_sqft": _area_ppsf(comps),
                "average_days_on_market": (
                    round(sum(doms) / len(doms), 1) if doms else None
                ),
                "comparables": comps,
                "disclaimer": DISCLAIMER,
            },
            indent=2,
        )

    @mcp.tool()
    def analyze_investment(
        price: float,
        monthly_rent: float,
        down_payment: float,
        annual_rate_pct: float = 6.5,
        term_years: int = 30,
        vacancy_rate: float = 0.05,
        annual_operating_expenses: float = 0.0,
    ) -> str:
        """Compute buy-and-hold investment metrics for a property.

        Returns NOI, cap rate, gross rent multiplier, monthly debt service,
        annual cash flow, and cash-on-cash return.
        """
        audit("analyze_investment", price=price, monthly_rent=monthly_rent)
        if price <= 0:
            return json.dumps({"error": "price must be positive."}, indent=2)
        metrics = investment_metrics(
            price=price,
            monthly_rent=monthly_rent,
            down_payment=down_payment,
            annual_rate_pct=annual_rate_pct,
            term_years=term_years,
            vacancy_rate=vacancy_rate,
            annual_operating_expenses=annual_operating_expenses,
        )
        metrics["disclaimer"] = DISCLAIMER
        return json.dumps(metrics, indent=2)

    @mcp.tool()
    def analyze_listing_investment(
        property_id: str,
        monthly_rent: float,
        down_payment_pct: float = 20.0,
        annual_rate_pct: float = 6.5,
        term_years: int = 30,
    ) -> str:
        """Run investment analysis on an existing listing using its list price.

        ``down_payment_pct`` is a percentage of the list price.
        """
        audit("analyze_listing_investment", property_id=property_id)
        prop = data.get_property_by_id(property_id)
        if not prop:
            return json.dumps(
                {"error": f"Property with ID {property_id} not found"}, indent=2
            )
        price = float(prop.get("price", 0) or 0)
        if price <= 0:
            return json.dumps({"error": "Listing has no usable price."}, indent=2)
        down_payment = price * (down_payment_pct / 100.0)
        metrics = investment_metrics(
            price=price,
            monthly_rent=monthly_rent,
            down_payment=down_payment,
            annual_rate_pct=annual_rate_pct,
            term_years=term_years,
        )
        metrics["property_id"] = property_id
        metrics["address"] = prop.get("address")
        metrics["down_payment_pct"] = down_payment_pct
        metrics["disclaimer"] = DISCLAIMER
        return json.dumps(metrics, indent=2)


def _assessment(delta_pct: Optional[float]) -> str:
    """Human-readable read on list price vs comparable estimate."""

    if delta_pct is None:
        return "Insufficient comparable data for an assessment."
    if delta_pct <= -5:
        return "List price is below comparable estimate (potentially underpriced)."
    if delta_pct >= 5:
        return "List price is above comparable estimate (potentially overpriced)."
    return "List price is in line with comparable sales."
