# Real Estate MCP Server — Workflow Examples

End-to-end examples showing how agents and AI assistants chain the Real Estate MCP
Server's tools, resources, and prompts into complete real estate workflows.

Each workflow follows a consistent five-step pattern:

```
User Request → AI Assistant → MCP Tool/Resource/Prompt Calls → Server Processing → Structured Response
```

All outputs are illustrative. The server provides workflow augmentation, not
financial, legal, or appraisal advice.

## 📋 Workflow Categories

- [🏠 Buyer affordability → shortlist → financing plan](#-buyer-affordability--shortlist--financing-plan)
- [📊 Comparable-based valuation of a listing](#-comparable-based-valuation-of-a-listing)
- [💰 Investment property analysis](#-investment-property-analysis)
- [🏘️ Neighborhood comparison & area intelligence](#️-neighborhood-comparison--area-intelligence)
- [🤝 Client matching & consultation](#-client-matching--consultation)
- [🏗️ Agent performance dashboard & strategy](#️-agent-performance-dashboard--strategy)
- [📄 Listing document ingestion & report export](#-listing-document-ingestion--report-export)
- [📥 Batch analysis via the async queue](#-batch-analysis-via-the-async-queue)
- [🔬 Deep property analysis via MCP sampling](#-deep-property-analysis-via-mcp-sampling)
- [🔌 Live data enrichment via optional integrations](#-live-data-enrichment-via-optional-integrations)
- [🔄 Workflow summary](#-workflow-summary)

---

## 🏠 Buyer Affordability → Shortlist → Financing Plan

### **Scenario**: A buyer earning $150k/year with $60k saved wants to know what they can afford, find matching properties, and understand their monthly costs

#### **Step 1: User Request**
```
Buyer's Agent: "My client earns $150k/year, has $60k for a down payment, and carries
$800/month in existing debt. What can they afford, and can you pull matching listings
with a full payment breakdown on the best option?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll run an affordability calculation first to establish a budget ceiling,
then filter the listings, and finally build out a full mortgage breakdown on the best-fit
property — including an amortization snapshot."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — affordability ceiling:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "estimate_affordability_tool",
    "arguments": {
      "annual_income": 150000,
      "monthly_debts": 800,
      "down_payment": 60000
    }
  }
}
```

**Tool Call 2 — filter within budget:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "filter_properties",
    "arguments": {
      "max_price": 620000,
      "min_bedrooms": 3
    }
  }
}
```

**Tool Call 3 — payment on the target property:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "calculate_mortgage_payment",
    "arguments": {
      "principal": 500000,
      "annual_rate_pct": 6.5,
      "term_years": 30
    }
  }
}
```

**Tool Call 4 — first-year amortization snapshot:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_amortization_schedule",
    "arguments": {
      "principal": 500000,
      "annual_rate_pct": 6.5,
      "term_years": 30,
      "max_rows": 12
    }
  }
}
```

**Tool Call 5 — compare 15yr vs 30yr (no dedicated "compare scenarios" tool
exists, so the assistant calls `calculate_mortgage_payment` a second time
with the 15-year terms and compares the two results itself):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "calculate_mortgage_payment",
    "arguments": {
      "principal": 500000,
      "annual_rate_pct": 6.0,
      "term_years": 15
    }
  }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "mortgage_planning_prompt",
    "arguments": {
      "annual_income": "150000",
      "monthly_debts": "800",
      "down_payment": "60000"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Finance engine** (`finance_helpers.py`) applies the 28/36 DTI rule to compute `max_purchase_price` and `max_loan_amount`
2. **Property tools** filter the seed data against price ceiling and bedroom count
3. **Mortgage calculator** computes P&I, taxes (estimated), and insurance (estimated) for the selected property
4. **Amortization engine** generates the month-by-month schedule for year 1
5. **Scenario comparator** produces side-by-side loan comparison
6. All results are audit-logged via `utils.audit()`

#### **Step 5: Response to Buyer's Agent**
```markdown
## Affordability & Financing Plan

### Budget Summary
| | Value |
|---|---|
| Annual income | $150,000 |
| Monthly debts | $800 |
| Down payment | $60,000 |
| **Max purchase price** | **$618,400** |
| Max loan amount | $558,400 |
| Est. monthly payment (P&I + T&I) | ~$3,820 |

### Matching Listings (3 found under $620k with 3+ beds)
| Property | Area | Price | Beds/Baths | Sqft |
|---|---|---|---|---|
| PROP003 — Canyon Crest Contemporary | Canyon Crest | $595,000 | 3/2 | 1,850 |
| PROP004 — Arlington Townhouse | Arlington Heights | $499,000 | 3/2.5 | 1,650 |
| PROP005 — La Sierra Family Home | La Sierra | $549,000 | 4/3 | 2,100 |

### Financing Breakdown — PROP003 ($595,000, 20% down = $500k loan)

**Monthly Payment (30yr @ 6.5%)**
| Component | Amount |
|---|---|
| Principal & Interest | $3,160 |
| Est. Property Tax (1.1%) | $546 |
| Est. Insurance | $124 |
| **Total est. monthly** | **$3,830** |

**Year 1 Amortization Snapshot (first 3 months)**
| Month | Payment | Principal | Interest | Balance |
|---|---|---|---|---|
| 1 | $3,160 | $452 | $2,708 | $499,548 |
| 2 | $3,160 | $455 | $2,705 | $499,093 |
| 3 | $3,160 | $457 | $2,703 | $498,636 |

**Loan Scenario Comparison**
| Scenario | Rate | Term | Monthly P&I | Total Interest |
|---|---|---|---|---|
| 30-year | 6.5% | 30 yr | $3,160 | $638,000 |
| 15-year | 6.0% | 15 yr | $4,219 | $259,000 |

*The 15-year saves ~$379k in interest but adds ~$1,059/month — confirm cash-flow comfort before recommending.*

### Recommended Next Steps
1. Lock in pre-approval at the $620k ceiling before showing PROP003/005
2. Verify property tax rates for Canyon Crest (currently estimated)
3. Discuss 15 vs 30 yr tradeoff with client at consultation
4. Schedule showings for PROP003 and PROP005 as top-of-budget options
```

---

## 📊 Comparable-Based Valuation of a Listing

### **Scenario**: A listing agent wants to know whether their $749k ask price for PROP001 is defensible before the open house

#### **Step 1: User Request**
```
Listing Agent: "I have PROP001 going live at $749,000 this weekend. Can you run a
comparable market analysis and tell me whether the price holds up against recent
sales in Downtown Riverside?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll pull a CMA-style valuation using recent area sales, compare the
implied price-per-sqft against the listing, and then layer in the broader market
context for Downtown Riverside."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — CMA valuation:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "estimate_property_value",
    "arguments": { "property_id": "PROP001" }
  }
}
```

**Tool Call 2 — recent sales comps:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_recent_sales",
    "arguments": { "area": "Downtown Riverside", "limit": 5 }
  }
}
```

**Resource Access — area market data:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://market/area/Downtown Riverside" }
}
```

**Resource Access — property insights:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://property/PROP001/insights" }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "valuation_prompt",
    "arguments": {
      "property_id": "PROP001",
      "area": "Downtown Riverside"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Valuation engine** retrieves PROP001's square footage and matches recent sales in the same area
2. Area average price-per-sqft is computed from the last 5 comparable transactions
3. Estimated value = sqft × avg $/sqft; variance from list price is flagged
4. Area market resource provides median prices, DOM, and trend direction
5. Property insights resource surfaces days-on-market benchmarks and feature premiums

#### **Step 5: Response to Listing Agent**
```markdown
## CMA Valuation — PROP001 (Downtown Riverside Victorian)

### Property Snapshot
| Field | Value |
|---|---|
| Address | 123 Heritage Lane, Downtown Riverside |
| List price | $749,000 |
| Bedrooms / Baths | 4 / 3 |
| Square footage | 2,200 sqft |
| Year built | 1915 (Victorian) |

### Comparable Sales (Downtown Riverside, last 90 days)
| Address | Sale Price | Sqft | $/Sqft | DOM |
|---|---|---|---|---|
| 88 Oak Street | $710,000 | 2,050 | $346 | 18 |
| 215 Magnolia Ave | $765,000 | 2,300 | $332 | 22 |
| 40 Elm Court | $698,000 | 1,980 | $353 | 14 |
| 7 Riverside Blvd | $740,000 | 2,150 | $344 | 20 |
| 110 Heritage Lane | $729,000 | 2,100 | $347 | 16 |

**Area average $/sqft:** $344

### Valuation Result
| | |
|---|---|
| Estimated value (CMA) | **$756,800** (2,200 × $344) |
| List price | $749,000 |
| Variance | **–$7,800 (–1.0%)** ✅ |
| Assessment | List price is **within normal range** of comps |

### Market Context — Downtown Riverside
- **Median sale price:** $738,000 | **Trend:** +3.2% YoY
- **Avg days on market:** 18 days
- **Inventory:** Low (seller's market)
- **Price reductions:** 8% of listings in last 60 days

### Pricing Recommendation
✅ $749,000 is **well-supported** by comps — within 1% of CMA estimate.
The Victorian character and 2,200 sqft position this at the upper end of
comparable $/sqft, which is justifiable given the low-inventory environment.

*If you see competing offers slow down after day 14, consider a $15k price
reduction before day 21 (area DOM average).*

### Next Steps
1. Confirm recent renovations / upgrades not captured in comp data
2. Flag the Victorian premium in the listing description
3. Re-run CMA if any new Downtown Riverside comp closes before weekend
```

---

## 💰 Investment Property Analysis

### **Scenario**: An investor wants to evaluate PROP002 as a buy-and-hold rental before making an offer

#### **Step 1: User Request**
```
Investor: "I'm looking at PROP002 — asking $850,000. I can put 25% down and think
I can get $3,500/month in rent. Walk me through the numbers: cap rate, cash flow,
and whether it's worth it versus my 7% hurdle rate."
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll run a full investment analysis — NOI, cap rate, gross rent
multiplier, cash-on-cash return, and monthly cash flow — then stack it against
your 7% hurdle rate and pull the area's rental market context."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — direct investment analysis:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "analyze_investment",
    "arguments": {
      "price": 850000,
      "monthly_rent": 3500,
      "down_payment": 212500
    }
  }
}
```

**Tool Call 2 — property-linked investment (uses seed data):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "analyze_investment",
    "arguments": {
      "property_id": "PROP002",
      "down_payment_pct": 25,
      "monthly_rent": 3500
    }
  }
}
```

**Tool Call 3 — area investment opportunities for context:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_investment_opportunities",
    "arguments": { "area": "Woodcrest" }
  }
}
```

**Resource Access:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://market/area/Woodcrest" }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "investment_analysis",
    "arguments": {
      "property_id": "PROP002",
      "investment_goal": "buy_and_hold_rental"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Finance engine** computes NOI (gross rent minus vacancy and operating expenses), cap rate, GRM, monthly mortgage service, annual cash flow, and cash-on-cash return
2. **Hurdle rate comparison** flags whether cash-on-cash return clears the stated threshold
3. Area market resource provides local rental demand signals and average days-to-rent data
4. Results are deterministic — same inputs always produce same outputs

#### **Step 5: Response to Investor**
```markdown
## Investment Analysis — PROP002 (Woodcrest Contemporary)

### Deal Parameters
| | |
|---|---|
| Purchase price | $850,000 |
| Down payment (25%) | $212,500 |
| Loan amount | $637,500 |
| Monthly rent (projected) | $3,500 |
| Mortgage (30yr @ 6.75%) | $4,134/month |

### Key Metrics
| Metric | Value | Benchmark |
|---|---|---|
| Gross annual rent | $42,000 | — |
| Vacancy allowance (5%) | –$2,100 | — |
| Operating expenses (est. 30%) | –$11,970 | — |
| **Net Operating Income (NOI)** | **$27,930** | — |
| **Cap rate** | **3.29%** | ⚠️ Area avg: 4.1% |
| **Gross Rent Multiplier (GRM)** | **20.2×** | Area avg: 18.5× |
| Debt service (annual) | $49,608 | — |
| **Annual cash flow** | **–$21,678** | 🔴 Negative |
| **Cash-on-cash return** | **–10.2%** | 🔴 Below 7% hurdle |

### Assessment
🔴 **This deal does not clear your 7% hurdle rate at current inputs.**

The cap rate (3.29%) is below the Woodcrest area average (4.1%), and
at $637,500 financed at 6.75%, the debt service exceeds rental income
by ~$1,806/month — resulting in negative annual cash flow.

**Scenarios that flip this to positive cash flow:**
| Lever | Required value |
|---|---|
| Higher rent | ≥ $5,200/month |
| Lower price | ≤ $620,000 |
| Larger down payment | ≥ 55% ($467,500) |
| Rate drop | ≤ 4.8% |

### Area Context — Woodcrest Rental Market
- Average rental yield in area: ~4.1% cap rate
- Avg days to lease: 21 days
- Rental demand trend: Stable (+1.8% YoY rent growth)

### Recommended Next Steps
1. Negotiate purchase price toward $750k–$780k before proceeding
2. Verify achievable rent with a local property manager (not just Zillow estimates)
3. Re-run analysis after any price reduction or rate lock confirmation
4. Consider PROP005 (La Sierra, $549k) as an alternative with better yield profile
```

---

## 🏘️ Neighborhood Comparison & Area Intelligence

### **Scenario**: A relocation buyer is deciding between two areas and needs a side-by-side breakdown covering schools, amenities, and market conditions

#### **Step 1: User Request**
```
Relocation Buyer: "We're moving from Seattle and have narrowed it down to
Canyon Crest or Woodcrest. We have two kids in elementary school. Can you give
me a full side-by-side comparison — schools, parks, shopping, healthcare, and
what the housing market looks like in each?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll pull comprehensive area reports for both neighborhoods,
extract school and amenity data specifically, and stack them side-by-side with
current market conditions so you have everything in one view."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — area comparison (both areas at once):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "compare_areas",
    "arguments": {
      "areas": ["Canyon Crest", "Woodcrest"]
    }
  }
}
```

**Tool Call 2 — school data, Canyon Crest:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_schools_data",
    "arguments": { "area": "Canyon Crest" }
  }
}
```

**Tool Call 3 — school data, Woodcrest:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_schools_data",
    "arguments": { "area": "Woodcrest" }
  }
}
```

**Tool Call 4 — comprehensive area report:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_comprehensive_area_report",
    "arguments": { "area": "Canyon Crest" }
  }
}
```

**Resource Access:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://all-areas" }
}
```

```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://amenities" }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "comparative_market_analysis",
    "arguments": {
      "areas": "Canyon Crest, Woodcrest",
      "buyer_priority": "schools, family amenities"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Area tools** pull demographics, walk score, commute data, and amenity counts from the seed data for each area
2. **Schools tool** extracts school names, ratings, type (public/private), and distance for each area
3. **Compare areas tool** builds the side-by-side diff across all dimensions
4. **Market tools** overlay median price, YoY appreciation, and days-on-market for each area

#### **Step 5: Response to Relocation Buyer**
```markdown
## Area Comparison — Canyon Crest vs. Woodcrest

### At a Glance
| | Canyon Crest | Woodcrest |
|---|---|---|
| Character | Hillside, suburban | Family-suburban |
| Median home price | $685,000 | $720,000 |
| YoY price growth | +4.1% | +2.8% |
| Avg days on market | 16 days | 22 days |
| Walkability score | 52 / 100 | 61 / 100 |
| Commute to Downtown | 18 min | 24 min |

### 🏫 Schools (Elementary Focus)
| School | Area | Rating | Type | Distance |
|---|---|---|---|---|
| Canyon Crest Academy | Canyon Crest | ⭐ 9/10 | Public | 0.8 mi |
| St. Francis Elementary | Canyon Crest | ⭐ 8/10 | Private | 1.2 mi |
| Woodcrest Elementary | Woodcrest | ⭐ 7/10 | Public | 0.5 mi |
| Heritage Charter | Woodcrest | ⭐ 8/10 | Charter | 1.4 mi |

**Canyon Crest** has the highest-rated elementary (9/10) in the dataset.

### 🌳 Parks & Outdoors
| | Canyon Crest | Woodcrest |
|---|---|---|
| Major parks | Canyon Rim Park, Sycamore Canyon | Woodcrest Regional Park |
| Trails within 2mi | 4 | 2 |
| Youth sports fields | 3 | 5 |

**Woodcrest** has more organized youth sports infrastructure.

### 🛒 Shopping & Daily Errands
| | Canyon Crest | Woodcrest |
|---|---|---|
| Grocery stores (≤1 mi) | 2 | 3 |
| Retail centers | 1 major plaza | 2 strip malls + 1 mall |
| Restaurant density | Moderate | High |

### 🏥 Healthcare
| | Canyon Crest | Woodcrest |
|---|---|---|
| Urgent care | 1 | 2 |
| Hospitals within 5mi | Riverside University Health | Loma Linda Medical Center |
| Pediatricians in area | 3 | 5 |

### Market Conditions
| | Canyon Crest | Woodcrest |
|---|---|---|
| Current inventory | 14 active listings | 21 active listings |
| Seller's/Buyer's market | Seller's | Balanced |
| Price reduction rate | 6% | 11% |

### Summary Recommendation
**For a family with elementary-age kids:**
- **Canyon Crest** wins on school ratings and appreciation pace — better for
  long-term value growth and top-tier public education
- **Woodcrest** wins on daily convenience, healthcare access, and youth sports —
  and offers slightly more negotiating room (11% price reduction rate)

If school ranking is the #1 priority → **Canyon Crest**.  
If lifestyle convenience and value are equally weighted → **Woodcrest**.

### Next Steps
1. Schedule a weekend drive-around in both areas
2. Request current school enrollment/waitlist status directly from each school
3. Filter listings in both areas under your budget using `filter_properties`
```

---

## 🤝 Client Matching & Consultation

### **Scenario**: An agent has a new client (CLI001) and wants to instantly surface matching listings and prepare a consultation brief

#### **Step 1: User Request**
```
Buyer's Agent: "CLI001 just came in — they're pre-approved to $750k, want 3+ beds,
prefer Canyon Crest or Downtown Riverside, and need good schools. Can you pull
matching properties and build me a consultation brief before our 3pm meeting?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll pull CLI001's full profile, run the preference-matching algorithm
against current listings, and build a structured consultation brief including
comparable properties and talking points."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — client profile:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_client_profile",
    "arguments": { "client_id": "CLI001" }
  }
}
```

**Tool Call 2 — preference matching:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "match_client_preferences",
    "arguments": { "client_id": "CLI001" }
  }
}
```

**Resource Access — pre-matched results:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://client/CLI001/matches" }
}
```

**Tool Call 3 — insights on top match:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_property_insights",
    "arguments": { "property_id": "PROP001" }
  }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "client_consultation",
    "arguments": {
      "client_id": "CLI001",
      "focus": "first_showing_prep"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Client tools** fetch CLI001's preferences (budget, areas, bedrooms, must-haves) from the seed data
2. **Matching algorithm** scores and ranks all active listings against weighted criteria
3. **Property insights** adds market context, days-on-market, and price-relative-to-area for top matches
4. **Consultation prompt** structures the output into a pre-meeting brief format

#### **Step 5: Response to Agent**
```markdown
## Client Consultation Brief — CLI001

### Client Profile
| Field | Value |
|---|---|
| Name | Michael & Sarah Thompson |
| Client since | 2024-11-01 |
| Pre-approval | $750,000 |
| Type | First-time buyer |
| Priority areas | Canyon Crest, Downtown Riverside |
| Min bedrooms | 3 |
| Must-haves | Good schools, garage, yard |
| Timeline | 60–90 days |

### Matched Listings (4 of 5 active properties match)

**🥇 Top Match — PROP001 (92% match score)**
| | |
|---|---|
| Address | 123 Heritage Lane, Downtown Riverside |
| Price | $749,000 |
| Bedrooms / Baths | 4 / 3 |
| Sqft | 2,200 |
| School rating | ⭐ 8.5/10 (Jefferson Elementary, 0.6mi) |
| Days on market | 12 |
| Vs. area median | +1.5% (fairly priced) |
| Garage | ✅ 2-car attached |
| Yard | ✅ 1,800 sqft backyard |

**🥈 Second Match — PROP003 (84% match score)**
| | |
|---|---|
| Address | 88 Summit Drive, Canyon Crest |
| Price | $595,000 |
| Bedrooms / Baths | 3 / 2 |
| Sqft | 1,850 |
| School rating | ⭐ 9/10 (Canyon Crest Academy, 0.8mi) |
| Days on market | 8 |
| Vs. area median | –13.1% (below median — value opportunity) |

**Other matches:** PROP004 ($499k, Arlington Heights, 3/2.5), PROP005 ($549k, La Sierra, 4/3)

### Consultation Talking Points
1. **Budget headroom:** Pre-approved at $750k; PROP001 at $749k leaves no buffer — explore PROP003 at $595k for negotiating room + top school rating
2. **School priority:** Canyon Crest Academy (9/10) at PROP003 outranks Downtown Riverside (8.5/10) at PROP001 — worth surfacing if schools are truly #1
3. **First-time buyer incentives:** Confirm whether client has explored CA first-time buyer programs (CalHFA, GSFA) — could affect loan structure
4. **Timeline:** 60–90 days aligns with current 16–22 day DOM in target areas — no urgency panic needed, but PROP003 is only 8 days on market

### Next Steps
1. Send showing requests for PROP001 (priority) and PROP003 (value alternative)
2. Confirm school enrollment windows with client before Canyon Crest vs. Downtown decision
3. Follow up with pre-approval letter before any offer
```

---

## 🏗️ Agent Performance Dashboard & Strategy

### **Scenario**: Agent Sarah Chen wants a full performance review before her quarterly business planning session

#### **Step 1: User Request**
```
Sarah Chen (Agent AG001): "Can you pull my full performance dashboard — sales,
active listings, client pipeline, and YTD numbers — and give me a strategy
brief for where to focus next quarter?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll load your dashboard, sales history, active property portfolio,
and client roster, then build a strategy brief against area market trends."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — agent dashboard:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_agent_dashboard",
    "arguments": { "agent_id": "AG001" }
  }
}
```

**Tool Call 2 — sales history:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_agent_sales",
    "arguments": { "agent_id": "AG001" }
  }
}
```

**Tool Call 3 — active client roster:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_agent_clients",
    "arguments": { "agent_id": "AG001" }
  }
}
```

**Tool Call 4 — market overview for context:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_market_overview",
    "arguments": {}
  }
}
```

**Resource Access:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://agent/AG001/dashboard" }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "agent_performance",
    "arguments": {
      "agent_id": "AG001",
      "period": "YTD",
      "focus": "quarterly_planning"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Agent tools** retrieve Sarah's profile, current listings, and transaction history from seed data
2. **Performance calculations** compute list-to-sale ratio, avg DOM, avg sale price, and pipeline value
3. **Market context** compares her metrics against area averages
4. **Strategy prompt** structures observations into a planning brief

#### **Step 5: Response to Agent**
```markdown
## Quarterly Performance Dashboard — Sarah Chen (AG001)

### YTD Summary
| Metric | Value | Area Avg |
|---|---|---|
| Closed transactions | 8 | — |
| Gross commission income (est.) | $198,400 | — |
| Avg sale price | $712,000 | $695,000 ✅ |
| List-to-sale ratio | 98.6% | 97.1% ✅ |
| Avg days on market | 14 days | 19 days ✅ |
| Active listings | 3 | — |
| Active buyer clients | 4 | — |

### Active Listing Portfolio
| Property | Area | List Price | DOM | Status |
|---|---|---|---|---|
| PROP001 — Heritage Victorian | Downtown Riverside | $749,000 | 12 | Active |
| PROP002 — Woodcrest Contemporary | Woodcrest | $850,000 | 6 | Active |
| PROP006 — Canyon Ridge Estate | Canyon Crest | $1,100,000 | 31 | ⚠️ Stale |

### Active Buyer Pipeline
| Client | Budget | Stage | Timeline |
|---|---|---|---|
| CLI001 — M. & S. Thompson | $750k | First showing | 60–90 days |
| CLI003 — R. Patel | $500k | Offer pending | Active |
| CLI004 — J. & L. Martinez | $900k | Area research | 90–120 days |
| CLI007 — A. Kim | $650k | Pre-approval stage | Unknown |

### Performance Highlights
✅ **Above-average:** Avg DOM (14 vs. 19 days), list-to-sale ratio (98.6% vs. 97.1%), avg sale price
⚠️ **Watch:** PROP006 at 31 DOM is approaching the Canyon Crest average (16 days) — price review warranted

### Q3 Strategy Brief

**1. Price review on PROP006**
At 31 DOM in a 16-day average market, Canyon Ridge Estate risks becoming a "stale
listing." A 3–5% reduction ($33k–$55k) or a fresh marketing push should be decided
before day 45.

**2. Convert CLI007 from passive to active**
A. Kim has no confirmed pre-approval or timeline. One check-in call to confirm
financing status could move this from "prospect" to "active buyer" in the pipeline.

**3. Double down on Downtown Riverside inventory**
Your avg sale price ($712k) skews above area median because of your DR concentration.
The area has <14 active listings and is trending seller's market — any new DR listing
mandate is high-leverage.

**4. Referral outreach**
8 closed deals YTD = 8 past clients. A quarterly "how's the home?" email to closed
clients from Q1–Q2 is one of the highest-ROI prospecting activities in low-inventory
markets.

### Next Steps
1. Call PROP006 seller this week to discuss DOM-based price strategy
2. Send pre-approval check-in to CLI007 before end of week
3. Set Google alerts for Downtown Riverside FSBO and expired listings
4. Block Q3 planning time to map referral outreach schedule
```

---

## 📄 Listing Document Ingestion & Report Export

### **Scenario**: An agent receives a listing information sheet as a `.txt` file from a seller and wants to ingest it, validate the data, and produce a formatted `.docx` report for their file

#### **Step 1: User Request**
```
Listing Coordinator: "The seller sent over their property details as a text file
(seller_listing_brief.txt). Can you pull the key fields out, and then generate a
formatted Word report I can attach to the listing file?"
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll ingest the text file to extract structured property data —
price, beds/baths, square footage, type, and address — then build a formatted
.docx report for your records."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — ingest the listing document:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "ingest_listing_document",
    "arguments": {
      "file_path": "/listings/seller_listing_brief.txt"
    }
  }
}
```

**Tool Call 2 — export formatted report:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "export_property_report",
    "arguments": {
      "report_json": "<structured JSON from step 1>",
      "output_path": "/reports/seller_listing_brief_report.docx"
    }
  }
}
```

#### **Step 4: Server Processing**
1. **Document tools** read the `.txt` file directly from disk (`.docx` is also supported via `python-docx`)
2. **Extraction heuristics** use regex patterns to identify price, bed/bath counts, square footage, year built, property type, and address
3. **Export tools** take the structured JSON and produce a formatted `.docx` using a standard report template
4. Fields that cannot be extracted return `null` — the tool never guesses

#### **Step 5: Response to Listing Coordinator**
```markdown
## Listing Ingestion — seller_listing_brief.txt

### Extracted Fields
| Field | Extracted Value | Confidence |
|---|---|---|
| Address | 88 Summit Drive, Canyon Crest, CA 92507 | ✅ High |
| List price | $595,000 | ✅ High |
| Bedrooms | 3 | ✅ High |
| Bathrooms | 2 | ✅ High |
| Square footage | 1,850 | ✅ High |
| Year built | 2003 | ✅ High |
| Property type | Single-family | ✅ High |
| Garage | 2-car attached | ✅ High |
| Lot size | 6,200 sqft | ⚠️ Medium |
| HOA fee | null | ❌ Not found in document |

*3 of 10 fields required manual confirmation (lot size ambiguous; HOA not mentioned).*

### Exported Report
✅ Formatted `.docx` report written to:
`/reports/seller_listing_brief_report.docx`

Report includes: property header, all extracted fields in a formatted table,
extraction confidence notes, and a blank "Agent Notes" section for manual additions.

### Next Steps
1. Open the `.docx` report and confirm lot size manually (two measurements referenced)
2. Contact seller about HOA status before MLS entry
3. Upload the report to the listing file management system
4. Use the extracted JSON as input for `estimate_property_value` to validate ask price
```

---

## 📥 Batch Analysis via the Async Queue

### **Scenario**: A property manager needs to risk-screen and analyze a batch of 10 incoming listing submissions overnight

#### **Step 1: User Request**
```
Property Manager: "I have 10 new listing submissions in the /intake folder. Queue
them all for analysis — I'll check the results first thing tomorrow morning."
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll queue each listing for analysis and give you job IDs for all
10 so you can pull status and results whenever you're ready. Jobs persist in the
local database — nothing is lost between sessions."
```

#### **Step 3: MCP Server Interactions**

**Tool Call — queue each listing (repeat for each file):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "queue_property_analysis",
    "arguments": {
      "file_path": "/intake/listing_07.txt",
      "analysis_notes": "Q3 batch intake — Canyon Crest submissions"
    }
  }
}
```

**Next morning — check all job statuses:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "list_analysis_jobs",
    "arguments": {}
  }
}
```

**Check one specific job:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_analysis_status",
    "arguments": { "job_id": "3f1c9e2a-84b1-4d2e-a9f7-c812e3047b66" }
  }
}
```

**Retrieve the full result:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_analysis_result",
    "arguments": { "job_id": "3f1c9e2a-84b1-4d2e-a9f7-c812e3047b66" }
  }
}
```

#### **Step 4: Server Processing**
1. Each `queue_property_analysis` call generates a UUID job ID, writes a `queued` record to local SQLite (`real_estate_mcp_analysis.db`), runs ingestion and analysis synchronously, then updates the record to `complete` or `error`
2. `list_analysis_jobs`, `get_analysis_status`, and `get_analysis_result` read from the same local store — no network calls, no external submission
3. The database is gitignored and persists across server restarts; it is not committed to the repository

#### **Step 5: Response to Property Manager**
```markdown
## Batch Analysis Queue — Q3 Intake (10 listings)

10 jobs queued. **9 complete, 1 error** (unsupported file type: `.pdf`).

### Job Summary
| Job ID (short) | File | Status | Est. Value | Notes |
|---|---|---|---|---|
| 3f1c9e2a | listing_01.txt | ✅ complete | $612,000 | Priced at $595k — below estimate |
| 7b4d0f11 | listing_02.txt | ✅ complete | $748,000 | Matches ask price |
| a92e88c0 | listing_03.txt | ✅ complete | $501,000 | Overpriced at $549k ⚠️ |
| d41c7e55 | listing_04.txt | ✅ complete | $695,000 | Within 2% of ask |
| 18f9a3b2 | listing_05.txt | ✅ complete | $831,000 | Below ask — value listing |
| 6c2d1e44 | listing_06.txt | ✅ complete | $423,000 | Fairly priced |
| 9a0f8c77 | listing_07.txt | ✅ complete | $558,000 | Matches ask |
| b33d9021 | listing_08.txt | ✅ complete | $719,000 | 4% above ask — strong value |
| e7f5120e | listing_09.txt | ✅ complete | $647,000 | Fairly priced |
| 2190a4dc | listing_10.pdf | ❌ error | — | Unsupported format |

### Flags for Immediate Attention
⚠️ **listing_03** — asking $549k vs. $501k estimate. May need price discussion with seller before MLS entry.

### Next Steps
1. Open `get_analysis_result` for listing_03 to review full extraction before calling the seller
2. Convert listing_10.pdf to `.txt` or `.docx` and re-queue
3. Export `.docx` reports for listings flagged for MLS submission this week
```

> **Note:** Job results are stored in a local SQLite database (`real_estate_mcp_analysis.db`)
> in the working directory. Nothing leaves your machine. The file is gitignored and is not
> committed to the repository.

---

## 🔬 Deep Property Analysis via MCP Sampling

### **Scenario**: An agent wants a deeper-than-heuristic analysis of PROP001 before a high-stakes listing presentation

#### **Step 1: User Request**
```
Senior Agent: "Before tomorrow's listing presentation for PROP001, I want the
deepest analysis the server can give — not just the data points, but actual
strategic reasoning about positioning, risks, and opportunity. Use sampling if
you can."
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "I'll run deep_analyze_property on PROP001. If the MCP client
supports sampling, I'll forward the property data to the connected LLM for
extended strategic reasoning on top of the deterministic heuristics. If sampling
isn't available, I'll return the full heuristic analysis with a note."
```

#### **Step 3: MCP Server Interactions**

**Tool Call — deep analysis with sampling:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "deep_analyze_property",
    "arguments": { "property_id": "PROP001" }
  }
}
```

**Resource Access — property insights for context:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://property/PROP001/insights" }
}
```

**Prompt Usage:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "property_analysis",
    "arguments": {
      "property_id": "PROP001",
      "analysis_depth": "full"
    }
  }
}
```

#### **Step 4: Server Processing**

**With sampling (client advertises `sampling` capability):**
1. Server collects PROP001's full data payload (price, specs, comps, area context, market trends)
2. Issues `sampling/createMessage` to the connected MCP client's LLM
3. LLM response (strategic reasoning) is appended to the deterministic heuristic output
4. Combined result returned with a `sampling_used: true` flag

**Without sampling (fallback — most clients today):**
1. Server runs the full deterministic heuristic analysis on PROP001
2. Returns the result with `sampling_used: false` and an explanatory note
3. No error — the output is still the most detailed heuristic analysis available

#### **Step 5: Response to Senior Agent**
```markdown
## Deep Property Analysis — PROP001 (Downtown Riverside Victorian)

*sampling_used: true — LLM reasoning appended below heuristic summary*

---

### Heuristic Analysis

**Valuation**
- CMA estimate: $756,800 | List price: $749,000 | Variance: –1.0% ✅ (within normal range)
- Area avg $/sqft: $344 | PROP001 implied $/sqft: $340 ✅

**Market Position**
- DOM: 12 days (area avg: 18) — performing above market pace ✅
- Inventory context: Only 14 active listings in Downtown Riverside — supply constrained ✅
- Recent price reductions in area: 8% — low — no distress signal ✅

**Risk Flags**
- Year built 1915: potential deferred maintenance, lead paint, galvanized plumbing — budget $15k–$30k contingency
- Victorian character limits buyer pool (not universally appealing) — broader marketing needed
- No HOA = full owner maintenance responsibility

---

### LLM Strategic Reasoning (via sampling)

**Positioning opportunity:** The 1915 Victorian character is both the listing's
greatest differentiator and its biggest marketing challenge. The highest-converting
buyers for this property are remote workers or dual-income professionals who place
a premium on architectural uniqueness and neighborhood walkability — not first-time
buyers comparing bedrooms-per-dollar. The listing description and photography brief
should emphasize provenance, the craftsman details, and the Downtown Riverside
revival narrative rather than competing on spec.

**Offer strategy risk:** At 12 DOM with the area averaging 18, there's no urgency
pressure yet. The agent should resist any impulse to signal eagerness. If an offer
arrives below $730k in the first two weeks, the correct response is a modest counter
at $745k — not a dramatic reduction — because the market data does not yet support
price pressure.

**Negotiating leverage:** The low inventory (14 listings) combined with the
above-average DOM performance gives the seller genuine leverage to hold price
through day 21. After day 25, a targeted price reduction of $10k–$15k is more
powerful than waiting longer, as the psychological "new listing" freshness will
have fully expired by then.

**Buyer pre-qualification note:** Given the age of the home and likely inspection
findings (1915 construction), the agent should proactively prepare a pre-inspection
report or a "known items" disclosure addendum. This prevents surprise re-negotiations
post-acceptance, which are the most common value leakage point on historic properties.

---

### Bottom Line for Listing Presentation
✅ Price is defensible — don't reduce pre-market  
⚠️ Marketing brief must lead with character, not comps  
⚠️ Prepare a proactive inspection/disclosure strategy  
🎯 Target buyer profile: design-forward professionals and heritage-home enthusiasts
```

> **Note on sampling:** Most MCP clients (including Cursor and Claude Desktop as of
> mid-2026) do not yet advertise sampling support. When sampling is unavailable,
> `deep_analyze_property` returns the full heuristic analysis plus a note — it does not
> return an error. The heuristic output alone is still the richest single-tool analysis
> available in the server.

---

## 🔌 Live Data Enrichment via Optional Integrations

### **Scenario**: An out-of-state buyer relocating to Downtown Riverside wants a due-diligence brief — flood risk, walkability, crime, environmental hazards, weather, current mortgage rates, and demographics — before flying in to tour PROP001

#### **Step 1: User Request**
```
Relocation Buyer: "I'm flying in next week to look at 1234 Mission Inn Ave in
Downtown Riverside. Before I book the trip, can you pull together everything you
can on flood risk, walkability, crime, environmental hazards, this week's weather,
current mortgage rates, and area demographics? I'd also love a live valuation
check if you can get one."
```

#### **Step 2: AI Assistant Processing**
```
AI Assistant: "All of that comes from optional, opt-in integrations that are off
by default — let me check integration_status first to see what's enabled. For
whichever free sources are on, I'll pull live data. RentCast and Zillow are
metered/paid, so I'll only call those if they're configured, and I'll say so
plainly if they're not — no surprise charges."
```

#### **Step 3: MCP Server Interactions**

**Tool Call 1 — check what's enabled before calling anything:**
```json
{
  "method": "tools/call",
  "params": { "name": "integration_status", "arguments": {} }
}
```

**Tool Call 2 — flood zone (FEMA, free/keyless):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_flood_zone",
    "arguments": { "lat": 33.982735, "lon": -117.373137 }
  }
}
```

**Tool Call 3 — walkability (Walk Score, free tier):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_walk_score",
    "arguments": {
      "address": "1234 Mission Inn Ave, Riverside, CA 92501",
      "lat": 33.982735,
      "lon": -117.373137
    }
  }
}
```

**Tool Call 4 — state crime trend (FBI Crime Data, free):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_crime_summary",
    "arguments": { "state_abbr": "CA", "offense": "violent-crime" }
  }
}
```

**Tool Call 5 — environmental hazards (EPA, free/keyless):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_environmental_hazards",
    "arguments": { "state_abbr": "CA" }
  }
}
```

**Tool Call 6 — this week's forecast (NOAA, free/keyless):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_weather_forecast",
    "arguments": { "lat": 33.982735, "lon": -117.373137 }
  }
}
```

**Tool Call 7 — current mortgage rate (FRED, free):**
```json
{
  "method": "tools/call",
  "params": { "name": "get_live_mortgage_rate", "arguments": {} }
}
```

**Tool Call 8 — area demographics (Census, free):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_live_demographics",
    "arguments": { "state_fips": "06" }
  }
}
```

**Tool Call 9 — live property record (RentCast, metered/paid):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "lookup_live_property",
    "arguments": { "address": "1234 Mission Inn Ave, Riverside, CA 92501" }
  }
}
```

**Tool Call 10 — live valuation check (Zillow, paid/enterprise):**
```json
{
  "method": "tools/call",
  "params": {
    "name": "lookup_live_zestimate",
    "arguments": { "address": "1234 Mission Inn Ave, Riverside, CA 92501" }
  }
}
```

**Resource Access — same status, as a resource instead of a tool call:**
```json
{
  "method": "resources/read",
  "params": { "uri": "realestate://integrations/status" }
}
```

#### **Step 4: Server Processing**
1. Every integration reads its `*_ENABLED` flag and (where required) its API key from the environment on each call — nothing is cached at startup, so toggling a flag takes effect on the next request
2. **Disabled or unconfigured sources make zero network calls.** They return a structured status payload (`enabled`, `configured`, `missing_settings`, a plain-language `message`) instead — this is what happened for RentCast and Zillow below, since no metered/paid credentials are configured in this example
3. **Enabled free sources hit the real API** and return live data — FEMA, Walk Score, FBI Crime Data, EPA, NOAA, FRED, and Census in this example
4. Every call is audit-logged locally via `utils.audit()`; API keys are never echoed back in any tool or resource response, enabled or not
5. Live-data failures (rate limits, bad coordinates, network errors) degrade to a clear `error` field — never a silent false success

#### **Step 5: Response to Relocation Buyer**
```markdown
## Due-Diligence Brief — 1234 Mission Inn Ave, Downtown Riverside, CA

### Integration Status (checked first — free sources enabled for this trip)
| Source | Enabled | Cost |
|---|---|---|
| FEMA (flood) | ✅ | Free |
| Walk Score | ✅ | Free up to 5,000 calls/day |
| FBI Crime Data | ✅ | Free |
| EPA (environmental) | ✅ | Free |
| NOAA (weather) | ✅ | Free |
| FRED (mortgage rates) | ✅ | Free |
| Census (demographics) | ✅ | Free |
| RentCast (property records) | ⬜ Not configured | Metered — may incur cost |
| Zillow (Zestimate) | ⬜ Not configured | Paid/enterprise — requires an approved data license |

### Flood Risk (FEMA)
Zone **X** — "Area of Minimal Flood Hazard," outside the Special Flood Hazard Area. Flood insurance is not federally required for this zone.

### Walkability
Walk Score **91** ("Walker's Paradise") · Transit Score **58** · Bike Score **72** — consistent with the listing's "walking distance to Mission Inn and downtown amenities" description.

### Crime Trend (California, trailing 12 months, FBI Crime Data Explorer)
Statewide violent-crime actuals have ranged from ~8,900 to ~15,400 incidents/month over the past year, with no sustained upward trend. *State-level context only — the tool does not yet support a city/radius-level crime query.*

### Environmental Hazards (EPA Toxics Release Inventory)
25 TRI-reporting facilities statewide returned for California; none in the immediate Downtown Riverside area in this sample. *State-level query only — cross-reference county/city fields for local relevance.*

### This Week's Weather (NOAA)
Overnight: 64°F, clear, light SW wind. Riverside's forecast this week is typical for the season — no severe weather advisories active.

### Current Mortgage Rate (FRED, Freddie Mac PMMS)
30-year fixed: **6.85%** as of the most recent weekly survey — plug this into `calculate_mortgage_payment` for an up-to-date payment estimate instead of an assumed rate.

### Area Demographics (Census ACS 5-Year, California)
Population ~39.0M · Median household income ~$84,000. *State-level in this example — pass a tract/county FIPS code for neighborhood-level figures.*

### Live Property Record (RentCast) — not available
RentCast is not configured for this session. Enable with `RENTCAST_ENABLED=true` and `RENTCAST_API_KEY` to pull a live property record and rent estimate (metered — understand the billing implications first).

### Live Valuation Check (Zillow) — not available
Zillow requires an approved, paid Zillow Group data license (e.g. Bridge Interactive, ~$500+/mo) — there is no public self-serve Zillow API. Enable with `ZILLOW_ENABLED=true` and `ZILLOW_API_KEY` once you have one.

### Next Steps
1. All flags above are green except the two paid sources — no additional setup needed for this brief
2. If a live AVM check matters before booking travel, weigh RentCast's metered cost against the value of an extra data point
3. Re-run `get_live_mortgage_rate` the morning of the offer — FRED's rate updates weekly
```

> **Note on cost and privacy:** every source in this workflow is **opt-in and off by
> default**. Nothing above required enabling a paid integration — seven of nine
> sources are free, and the two paid ones (RentCast, Zillow) clearly self-report
> as unconfigured rather than silently failing or incurring a surprise charge.
> See [`integrations/README.md`](integrations/README.md) for the full enable/cost
> table and its live spec-verification notes.

---

## 🔄 Workflow Summary

### Common Patterns Across All Workflows

Every workflow above follows the same five-step structure:

1. **User Request** — a concrete, role-specific need from an agent, buyer, investor, or coordinator
2. **AI Processing** — the assistant selects and sequences the right tools
3. **MCP Server Interactions** — tools, resources, and prompts called with precise arguments
4. **Server Processing** — deterministic engines (finance, valuation, matching) produce consistent outputs
5. **Structured Response** — actionable, formatted deliverable ready for the next real-world step

### Tool → Workflow Matrix

| Workflow | Core tools used | Prompt used |
|---|---|---|
| Buyer financing plan | `estimate_affordability_tool`, `filter_properties`, `calculate_mortgage_payment`, `get_amortization_schedule` | `mortgage_planning_prompt` |
| CMA valuation | `estimate_property_value`, `get_recent_sales` | `valuation_prompt` |
| Investment analysis | `analyze_investment`, `get_investment_opportunities` | `investment_analysis` |
| Neighborhood comparison | `compare_areas`, `get_schools_data`, `get_comprehensive_area_report` | `comparative_market_analysis` |
| Client matching | `get_client_profile`, `match_client_preferences`, `get_property_insights` | `client_consultation` |
| Agent dashboard | `get_agent_dashboard`, `get_agent_sales`, `get_agent_clients`, `get_market_overview` | `agent_performance` |
| Document ingestion | `ingest_listing_document`, `export_property_report` | — |
| Batch queue | `queue_property_analysis`, `list_analysis_jobs`, `get_analysis_result` | — |
| Deep analysis | `deep_analyze_property` | `property_analysis` |
| Live integrations | `integration_status`, `get_live_flood_zone`, `get_live_walk_score`, `get_live_crime_summary`, `get_live_environmental_hazards`, `get_live_weather_forecast`, `get_live_mortgage_rate`, `get_live_demographics`, `lookup_live_property`, `lookup_live_zestimate` | — |

### Key Benefits

✅ **Composable** — tools chain together; the output of one (e.g., affordability ceiling) becomes the input of the next (property filter)  
✅ **Deterministic** — same inputs always produce same outputs; the finance and valuation engines are pure functions  
✅ **Offline-first** — all workflows above run fully offline; live data (Census, Walk Score, FEMA, FRED, FBI Crime Data, EPA, NOAA — free; RentCast, Zillow — paid/metered) is opt-in and additive  
✅ **Audited** — every tool call writes an audit record via `utils.audit()` for provenance and compliance  
✅ **Format-ready** — outputs are structured Markdown and JSON — easy to pipe into reports, emails, or CRMs  

---

*Built with the [Model Context Protocol](https://modelcontextprotocol.io).
Provides workflow augmentation, not financial, legal, or appraisal advice.*
