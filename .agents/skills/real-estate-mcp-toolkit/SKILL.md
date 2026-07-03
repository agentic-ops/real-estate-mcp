---
name: real-estate-mcp-toolkit
description: >-
  Teaches an agent the methodology for chaining the Real Estate MCP Server's
  50+ tools into complete workflows — buyer affordability and financing plans,
  comparable-based valuation, investment analysis, listing-document ingestion
  and report export, batch analysis, area/market intelligence, and deep
  property analysis. Use whenever the Real Estate MCP Server is connected and
  the user asks to search or evaluate properties, plan a mortgage, estimate a
  home's value, analyze a rental as an investment, ingest a listing sheet, or
  compare areas.
compatibility: Requires the Real Estate MCP Server (this repository) connected as an MCP server.
---

# Real Estate MCP Toolkit

The Real Estate MCP Server gives an agent 50+ tools across property, agent,
market, client, area, mortgage, valuation, document, analysis-queue,
integration, and system categories. Tools are the **execution layer** — this
skill is the **methodology layer**: which tools to call, in what order, and
what to surface. It provides workflow augmentation, not financial or appraisal
advice; every financial workflow ends with a disclaimer, not a guarantee.

## Non-negotiable rules

1. **Never present estimates as guarantees or appraisals.** Mortgage,
   valuation, and investment tools include a `disclaimer` field — always
   surface it.
2. **Prefer local, offline tools first.** `lookup_live_property` (RentCast) is
   opt-in and **metered** (may incur cost); `get_live_demographics` (Census)
   is opt-in too. Use local `estimate_property_value`,
   `comparable_market_analysis`, and the seed data unless the user needs live
   external data.
3. **Real files over seed IDs when a file exists.** If the user has an actual
   `.txt`/`.docx` listing, use `ingest_listing_document` rather than assuming a
   seed `property_id`.
4. **Respect feature flags.** Categories can be disabled via
   `REALESTATE_MCP_ENABLE_*`. If a tool is missing, read
   `realestate://server-config` before assuming the server is broken.
5. **State assumptions on every financial calc.** Rate, term, DTI, vacancy,
   and down payment drive the numbers — surface them (they are in the
   `assumptions` field).

## Tool quick reference

| Category | Tools |
| --- | --- |
| Property | `search_properties`, `filter_properties`, `get_property_details`, `get_property_insights` |
| Agent | `get_agent_dashboard`, `get_agent_properties`, `get_agent_sales` |
| Market | `get_market_overview`, `compare_areas`, `get_price_analytics`, `get_recent_sales` |
| Client | `get_client_details`, `match_client_preferences` |
| Area | `get_comprehensive_area_report`, `get_area_amenities`, `get_schools_data` |
| Mortgage | `calculate_mortgage_payment`, `get_amortization_schedule`, `estimate_affordability_tool`, `compare_refinance` |
| Valuation | `estimate_property_value`, `comparable_market_analysis`, `analyze_investment`, `analyze_listing_investment`, `deep_analyze_property` |
| Document | `ingest_listing_document`, `compare_listing_documents`, `export_property_report` |
| Analysis Queue | `queue_property_analysis`, `get_analysis_status`, `get_analysis_result`, `list_analysis_jobs` |
| Integrations | `integration_status`, `lookup_live_property`, `get_live_demographics` |
| System | `get_server_info`, `refresh_data`, `get_data_summary` |

Full worked examples: [WORKFLOW_EXAMPLES.md](../../../WORKFLOW_EXAMPLES.md).

## Workflow patterns

### 1. Buyer affordability & financing
**Trigger:** "how much house can I afford", "what's my monthly payment"

1. `estimate_affordability_tool(annual_income, monthly_debts, down_payment)` →
   max price and loan.
2. `filter_properties(max_price, min_bedrooms, ...)` → shortlist in budget.
3. `calculate_mortgage_payment(principal, annual_rate_pct, term_years)` for the
   target loan; `get_amortization_schedule` for the principal/interest split.
4. Use `compare_refinance` if the user already owns and asks about refinancing.
5. Close with the `disclaimer` and the assumptions used.

### 2. Comparable-based valuation
**Trigger:** "what's this home worth", "is it priced right"

1. `estimate_property_value(property_id)` → CMA-style estimate vs. list price.
2. `comparable_market_analysis(area)` → ground the estimate in recent comps.
3. Surface the `assessment` (under/over/fairly priced) and its basis.

### 3. Investment analysis
**Trigger:** "is this a good rental", "cap rate / cash flow"

1. For a hypothetical: `analyze_investment(price, monthly_rent, down_payment)`.
2. For an existing listing: `analyze_listing_investment(property_id,
   monthly_rent, down_payment_pct)`.
3. Report cap rate, cash-on-cash, and annual cash flow with the assumptions.

### 4. Listing-document ingestion & report
**Trigger:** "read this listing sheet", "make a report"

1. `ingest_listing_document(file_path)` (`.txt`/`.docx`) → structured fields.
2. `export_property_report(report_json, output_path.docx)` for a deliverable.
3. `compare_listing_documents(a, b)` to diff two sheets.

### 5. Batch / async analysis
**Trigger:** "analyze these listings", "queue this batch"

1. `queue_property_analysis(file_path, analysis_notes)` → `job_id`.
2. Poll `get_analysis_status(job_id)`; retrieve `get_analysis_result(job_id)`.
3. `list_analysis_jobs()` for a batch summary. Results persist in local SQLite.

### 6. Deep property analysis
**Trigger:** "give me a deeper read on this property"

1. `deep_analyze_property(property_id, focus)` — uses MCP sampling when the
   client supports it, otherwise returns the deterministic heuristic summary
   (with a note). Surface the `disclaimer`.

### 7. Area & market intelligence
**Trigger:** "tell me about this neighborhood", "compare these areas"

1. `get_comprehensive_area_report(area)` for a full picture.
2. `compare_areas("A,B,C")` and `get_market_overview` for context.
3. Only use `get_live_demographics` if the free Census integration is enabled
   (`integration_status`).

## Response shape

Close every financial/valuation workflow with:
- The `disclaimer` text verbatim from the tool response.
- The assumptions used (rate, term, DTI, vacancy, down payment).
- Concrete next steps (adjust inputs, pull comps, consult a lender/appraiser).
