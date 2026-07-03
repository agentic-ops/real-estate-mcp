"""Unit tests for the deterministic finance helpers."""

import pytest

from tools.finance_helpers import (
    amortization_schedule,
    amortization_summary,
    cap_rate,
    estimate_affordability,
    gross_rent_multiplier,
    investment_metrics,
    monthly_mortgage_payment,
    net_operating_income,
)


class TestMonthlyMortgagePayment:
    def test_standard_30_year(self):
        # $100k at 6% for 30 years -> ~$599.55/month.
        payment = monthly_mortgage_payment(100_000, 6.0, 30)
        assert payment == pytest.approx(599.55, abs=0.05)

    def test_zero_interest_is_straight_line(self):
        # $120k at 0% over 10 years (120 months) -> exactly $1000.
        payment = monthly_mortgage_payment(120_000, 0.0, 10)
        assert payment == pytest.approx(1000.0)

    def test_zero_principal(self):
        assert monthly_mortgage_payment(0, 6.0, 30) == 0.0

    def test_invalid_term_raises(self):
        with pytest.raises(ValueError):
            monthly_mortgage_payment(100_000, 6.0, 0)

    def test_higher_rate_costs_more(self):
        low = monthly_mortgage_payment(300_000, 4.0, 30)
        high = monthly_mortgage_payment(300_000, 8.0, 30)
        assert high > low


class TestAmortizationSummary:
    def test_totals_consistent(self):
        summary = amortization_summary(200_000, 6.0, 30)
        assert summary["number_of_payments"] == 360
        assert summary["principal"] == 200_000
        # total_paid = payment * n; total_interest = total_paid - principal.
        assert summary["total_interest"] == pytest.approx(
            summary["total_paid"] - 200_000, abs=0.01
        )
        assert summary["total_interest"] > 0

    def test_zero_interest_no_interest(self):
        summary = amortization_summary(120_000, 0.0, 10)
        assert summary["total_interest"] == pytest.approx(0.0, abs=0.01)


class TestAmortizationSchedule:
    def test_balance_reaches_zero(self):
        rows = amortization_schedule(50_000, 5.0, 5)
        assert len(rows) == 60
        assert rows[-1]["balance"] == pytest.approx(0.0, abs=0.5)

    def test_max_rows_truncates(self):
        rows = amortization_schedule(50_000, 5.0, 30, max_rows=12)
        assert len(rows) == 12
        # First month interest = balance * monthly rate.
        assert rows[0]["interest"] == pytest.approx(50_000 * (5.0 / 100 / 12), abs=0.01)

    def test_principal_grows_over_time(self):
        rows = amortization_schedule(50_000, 5.0, 30, max_rows=24)
        assert rows[-1]["principal"] > rows[0]["principal"]


class TestAffordability:
    def test_returns_positive_price(self):
        result = estimate_affordability(
            annual_income=120_000,
            monthly_debts=500,
            down_payment=60_000,
            annual_rate_pct=6.5,
        )
        assert result["max_purchase_price"] > result["down_payment"]
        assert result["max_loan_amount"] > 0

    def test_high_debts_consume_budget(self):
        result = estimate_affordability(
            annual_income=60_000,
            monthly_debts=5_000,
            down_payment=0,
            annual_rate_pct=6.5,
        )
        assert result["max_loan_amount"] == 0.0

    def test_higher_income_affords_more(self):
        low = estimate_affordability(80_000, 0, 0, 6.5)
        high = estimate_affordability(200_000, 0, 0, 6.5)
        assert high["max_purchase_price"] > low["max_purchase_price"]


class TestInvestmentMetrics:
    def test_net_operating_income(self):
        # $36k rent, 5% vacancy, $6k expenses -> 36000*0.95 - 6000 = 28200.
        assert net_operating_income(36_000, 0.05, 6_000) == pytest.approx(28_200)

    def test_cap_rate(self):
        assert cap_rate(50_000, 1_000_000) == 5.0
        assert cap_rate(50_000, 0) is None

    def test_gross_rent_multiplier(self):
        assert gross_rent_multiplier(500_000, 50_000) == 10.0
        assert gross_rent_multiplier(500_000, 0) is None

    def test_investment_metrics_shape(self):
        metrics = investment_metrics(
            price=500_000,
            monthly_rent=3_000,
            down_payment=100_000,
            annual_rate_pct=6.5,
        )
        assert metrics["cap_rate_pct"] is not None
        assert metrics["loan_amount"] == pytest.approx(400_000)
        assert "cash_on_cash_return_pct" in metrics
        assert metrics["annual_gross_rent"] == pytest.approx(36_000)

    def test_zero_down_payment_coc_none(self):
        metrics = investment_metrics(500_000, 3_000, 0, 6.5)
        assert metrics["cash_on_cash_return_pct"] is None
