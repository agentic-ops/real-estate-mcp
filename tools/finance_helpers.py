"""Shared, deterministic real-estate finance calculations.

Every function here is pure (no I/O, no network) so results can be audited
and unit-tested exactly. These helpers back the mortgage and valuation tools
and are intentionally transparent -- no opaque models.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def monthly_rate(annual_rate_pct: float) -> float:
    """Convert an annual percentage rate to a monthly decimal rate."""

    return (annual_rate_pct / 100.0) / 12.0


def monthly_mortgage_payment(
    principal: float,
    annual_rate_pct: float,
    term_years: int,
) -> float:
    """Standard fixed-rate amortized monthly principal + interest payment.

    Uses the annuity formula. A 0% rate degrades gracefully to a straight
    line (principal / number of payments).
    """

    n = int(term_years) * 12
    if n <= 0:
        raise ValueError("term_years must be positive")
    if principal <= 0:
        return 0.0
    r = monthly_rate(annual_rate_pct)
    if r == 0:
        return principal / n
    factor = (1 + r) ** n
    return principal * (r * factor) / (factor - 1)


def amortization_summary(
    principal: float,
    annual_rate_pct: float,
    term_years: int,
) -> Dict[str, Any]:
    """Return payment, total paid, and total interest over the loan life."""

    payment = monthly_mortgage_payment(principal, annual_rate_pct, term_years)
    n = int(term_years) * 12
    total_paid = payment * n
    return {
        "monthly_payment": round(payment, 2),
        "number_of_payments": n,
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_paid - principal, 2),
        "principal": round(principal, 2),
    }


def amortization_schedule(
    principal: float,
    annual_rate_pct: float,
    term_years: int,
    max_rows: Optional[int] = None,
) -> List[Dict[str, float]]:
    """Generate a per-month amortization schedule.

    ``max_rows`` optionally truncates the returned rows (the math still runs
    for the full term so balances remain accurate).
    """

    payment = monthly_mortgage_payment(principal, annual_rate_pct, term_years)
    r = monthly_rate(annual_rate_pct)
    n = int(term_years) * 12
    balance = float(principal)
    rows: List[Dict[str, float]] = []
    for month in range(1, n + 1):
        interest = balance * r
        principal_paid = payment - interest
        balance = max(0.0, balance - principal_paid)
        if max_rows is None or month <= max_rows:
            rows.append(
                {
                    "month": month,
                    "payment": round(payment, 2),
                    "principal": round(principal_paid, 2),
                    "interest": round(interest, 2),
                    "balance": round(balance, 2),
                }
            )
    return rows


def estimate_affordability(
    annual_income: float,
    monthly_debts: float,
    down_payment: float,
    annual_rate_pct: float,
    term_years: int = 30,
    max_dti: float = 0.36,
    property_tax_rate_pct: float = 1.1,
    annual_insurance: float = 1200.0,
) -> Dict[str, Any]:
    """Estimate the maximum affordable purchase price from income and DTI.

    Works backwards from the monthly budget available for housing (income *
    max_dti minus existing debts) to a supportable loan principal, then adds
    the down payment. Taxes and insurance are folded into the monthly budget.
    """

    monthly_income = annual_income / 12.0
    housing_budget = monthly_income * max_dti - monthly_debts
    monthly_insurance = annual_insurance / 12.0
    available_for_piti = max(0.0, housing_budget)

    # Approximate monthly tax + a share of P&I. Solve for principal using the
    # inverse annuity factor, treating taxes as a fraction of price.
    r = monthly_rate(annual_rate_pct)
    n = int(term_years) * 12
    monthly_tax_rate = (property_tax_rate_pct / 100.0) / 12.0

    budget_after_insurance = max(0.0, available_for_piti - monthly_insurance)
    if budget_after_insurance <= 0:
        return {
            "max_purchase_price": round(down_payment, 2),
            "max_loan_amount": 0.0,
            "estimated_monthly_payment": 0.0,
            "monthly_housing_budget": round(available_for_piti, 2),
            "note": "Existing debts consume the housing budget at this DTI.",
        }

    if r == 0:
        pi_factor = 1.0 / n
    else:
        factor = (1 + r) ** n
        pi_factor = (r * factor) / (factor - 1)

    # payment = principal * pi_factor + price * monthly_tax_rate
    # price = principal + down_payment  => solve for principal.
    denominator = pi_factor + monthly_tax_rate
    principal = (budget_after_insurance - down_payment * monthly_tax_rate) / denominator
    principal = max(0.0, principal)
    price = principal + down_payment
    payment = monthly_mortgage_payment(principal, annual_rate_pct, term_years)
    monthly_tax = price * monthly_tax_rate
    return {
        "max_purchase_price": round(price, 2),
        "max_loan_amount": round(principal, 2),
        "down_payment": round(down_payment, 2),
        "estimated_monthly_payment": round(
            payment + monthly_tax + monthly_insurance, 2
        ),
        "principal_and_interest": round(payment, 2),
        "monthly_property_tax": round(monthly_tax, 2),
        "monthly_insurance": round(monthly_insurance, 2),
        "monthly_housing_budget": round(available_for_piti, 2),
        "assumptions": {
            "max_dti": max_dti,
            "term_years": term_years,
            "annual_rate_pct": annual_rate_pct,
            "property_tax_rate_pct": property_tax_rate_pct,
            "annual_insurance": annual_insurance,
        },
    }


def net_operating_income(
    annual_rent: float,
    vacancy_rate: float = 0.05,
    annual_operating_expenses: float = 0.0,
) -> float:
    """Net operating income: gross rent less vacancy and operating expenses."""

    effective_rent = annual_rent * (1 - vacancy_rate)
    return effective_rent - annual_operating_expenses


def cap_rate(noi: float, price: float) -> Optional[float]:
    """Capitalization rate (NOI / price) as a percentage."""

    if price <= 0:
        return None
    return round((noi / price) * 100.0, 2)


def gross_rent_multiplier(price: float, annual_rent: float) -> Optional[float]:
    """Gross rent multiplier (price / annual gross rent)."""

    if annual_rent <= 0:
        return None
    return round(price / annual_rent, 2)


def investment_metrics(
    price: float,
    monthly_rent: float,
    down_payment: float,
    annual_rate_pct: float,
    term_years: int = 30,
    vacancy_rate: float = 0.05,
    annual_operating_expenses: float = 0.0,
) -> Dict[str, Any]:
    """Compute the common buy-and-hold investment return metrics."""

    annual_rent = monthly_rent * 12.0
    noi = net_operating_income(annual_rent, vacancy_rate, annual_operating_expenses)
    loan = max(0.0, price - down_payment)
    monthly_pi = monthly_mortgage_payment(loan, annual_rate_pct, term_years)
    annual_debt_service = monthly_pi * 12.0
    annual_cash_flow = noi - annual_debt_service
    coc = (
        round((annual_cash_flow / down_payment) * 100.0, 2)
        if down_payment > 0
        else None
    )
    return {
        "price": round(price, 2),
        "monthly_rent": round(monthly_rent, 2),
        "annual_gross_rent": round(annual_rent, 2),
        "net_operating_income": round(noi, 2),
        "cap_rate_pct": cap_rate(noi, price),
        "gross_rent_multiplier": gross_rent_multiplier(price, annual_rent),
        "loan_amount": round(loan, 2),
        "monthly_debt_service": round(monthly_pi, 2),
        "annual_debt_service": round(annual_debt_service, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cash_on_cash_return_pct": coc,
        "assumptions": {
            "down_payment": round(down_payment, 2),
            "annual_rate_pct": annual_rate_pct,
            "term_years": term_years,
            "vacancy_rate": vacancy_rate,
            "annual_operating_expenses": round(annual_operating_expenses, 2),
        },
    }
