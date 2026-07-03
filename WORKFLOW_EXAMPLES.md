# Workflow Examples

End-to-end examples showing how the Real Estate MCP Server's tools compose
into real workflows. Tool calls are shown as JSON-RPC `tools/call` params;
your MCP client (Claude Desktop, MCP Inspector, a custom client) issues them.

All outputs are illustrative. The server provides workflow augmentation, not
financial, legal, or appraisal advice.

---

## 1. Buyer affordability → shortlist → financing plan

**Goal:** help a buyer earning $150k with $60k down find and finance a home.

1. **Affordability**

   ```json
   {"name": "estimate_affordability_tool",
    "arguments": {"annual_income": 150000, "monthly_debts": 800, "down_payment": 60000}}
   ```

   Returns `max_purchase_price`, `max_loan_amount`, and an estimated monthly
   payment (P&I + taxes + insurance).

2. **Shortlist within budget**

   ```json
   {"name": "filter_properties",
    "arguments": {"max_price": 620000, "min_bedrooms": 3}}
   ```

3. **Payment for the target loan**

   ```json
   {"name": "calculate_mortgage_payment",
    "arguments": {"principal": 500000, "annual_rate_pct": 6.5, "term_years": 30}}
   ```

4. **Amortization insight**

   ```json
   {"name": "get_amortization_schedule",
    "arguments": {"principal": 500000, "annual_rate_pct": 6.5, "term_years": 30, "max_rows": 12}}
   ```

Use the `mortgage_planning_prompt` to have the assistant run this sequence and
summarize a price range and monthly budget.

---

## 2. Comparable-based valuation of a listing

**Goal:** decide whether `PROP001` is fairly priced.

1. **CMA-style estimate**

   ```json
   {"name": "estimate_property_value", "arguments": {"property_id": "PROP001"}}
   ```

   Multiplies the listing's square footage by the area's average
   price-per-square-foot from recent sales and compares to the list price.

2. **Ground it in comps**

   ```json
   {"name": "comparable_market_analysis", "arguments": {"area": "Downtown Riverside"}}
   ```

The `valuation_prompt` orchestrates both plus an investment read.

---

## 3. Investment analysis

**Goal:** evaluate a rental at $500k with $3,000/mo rent and $100k down.

```json
{"name": "analyze_investment",
 "arguments": {"price": 500000, "monthly_rent": 3000, "down_payment": 100000}}
```

Returns NOI, cap rate, gross rent multiplier, monthly debt service, annual
cash flow, and cash-on-cash return. For an existing listing, use
`analyze_listing_investment` with `property_id` and a `down_payment_pct`.

---

## 4. Ingest a listing sheet and export a report

1. **Ingest** a `.txt`/`.docx` listing:

   ```json
   {"name": "ingest_listing_document", "arguments": {"file_path": "/path/to/listing.txt"}}
   ```

   Extracts price, beds/baths, square footage, year built, type, and address.

2. **Export** a `.docx` report from the ingested JSON:

   ```json
   {"name": "export_property_report",
    "arguments": {"report_json": "<json from step 1>", "output_path": "/tmp/report.docx"}}
   ```

---

## 5. Batch analysis via the async queue

```json
{"name": "queue_property_analysis", "arguments": {"file_path": "/path/to/listing.txt"}}
```

Returns a `job_id`. Retrieve with `get_analysis_status` and
`get_analysis_result`; list everything with `list_analysis_jobs`. Results are
persisted in a local SQLite database (`real_estate_mcp_analysis.db`).

---

## 6. Deep analysis via MCP sampling

```json
{"name": "deep_analyze_property", "arguments": {"property_id": "PROP001"}}
```

If the connected client advertises **sampling** capability, the tool asks the
client's LLM for deeper reasoning on top of the data heuristics. Otherwise it
returns the deterministic heuristic summary only (with a note).

---

## 7. Optional live data (off by default)

Check status without enabling anything:

```json
{"name": "integration_status", "arguments": {}}
```

To enable the free Census demographic lookups, set `CENSUS_ENABLED=true`; to
enable RentCast property lookups, set `RENTCAST_ENABLED=true` and
`RENTCAST_API_KEY`. RentCast is metered and may incur costs.
