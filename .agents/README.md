# .agents/

Vendor-agnostic agent skills — reusable workflow definitions compatible with
Cursor, Claude Code, Codex CLI, Gemini CLI, and other compliant LLM tools.

Skills complement MCP tools by providing **methodology**: which tools to
chain, in what order, and what to surface to the user. The MCP server is the
**execution layer** (50+ tools); a skill is the **playbook layer**. Connecting
the server alone gives an agent tools without a playbook; the skill is the
playbook.

## Skills

### [`skills/real-estate-mcp-toolkit/SKILL.md`](skills/real-estate-mcp-toolkit/SKILL.md)

Teaches an agent the methodology for chaining the Real Estate MCP Server's
tools into complete workflows:

- **Buyer affordability & financing** — `estimate_affordability_tool` →
  `filter_properties` → `calculate_mortgage_payment` → `get_amortization_schedule`
- **Comparable-based valuation** — `estimate_property_value` →
  `comparable_market_analysis`
- **Investment analysis** — `analyze_investment` / `analyze_listing_investment`
- **Listing ingestion & report** — `ingest_listing_document` →
  `export_property_report`
- **Batch analysis** — `queue_property_analysis` → poll → `get_analysis_result`
- **Deep analysis** — `deep_analyze_property` with MCP sampling fallback
- **Area & market intelligence** — `get_comprehensive_area_report`, `compare_areas`

The skill also encodes non-negotiable rules (never present estimates as
guarantees; prefer local tools and free live integrations over
metered/paid ones; always surface assumptions and disclaimers).

## Standard and compatibility

Skills follow the [Agent Skills open specification](https://agentskills.io/specification.md).
The same `SKILL.md` works unchanged across Claude Code, Cursor, Codex CLI, and
Gemini CLI. Cursor and Codex CLI discover skills under `.agents/skills/`
automatically. For Claude Code, symlink or copy the `real-estate-mcp-toolkit/`
directory into `.claude/skills/`.

## Adding a new skill

1. Create a directory under `.agents/skills/my-skill-name/`.
2. Add a `SKILL.md` with a YAML front matter block (`name`, `description`,
   `compatibility`) and the workflow methodology in the body.
3. Reference tool names by their exact MCP identifiers so agents can resolve
   them at runtime.
