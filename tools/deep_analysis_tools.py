"""Deep property analysis via MCP LLM sampling with heuristic fallback.

Asks the connected client's LLM to reason about a property (using MCP
sampling) and falls back to a deterministic, data-driven heuristic summary
when the client does not support sampling.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from mcp import types
from mcp.server.mcpserver import Context, MCPServer

from utils import audit, get_data_manager

_SAMPLING_CAPABILITY = types.ClientCapabilities(sampling=types.SamplingCapability())
DISCLAIMER = "AI-generated reasoning for review only. Not financial advice."
_SAMPLING_UNAVAILABLE_NOTE = (
    "Connected MCP client does not support LLM sampling; returning "
    "data-driven heuristic analysis only."
)


def _heuristic_summary(data, property_id: str) -> Dict[str, Any]:
    """Build a deterministic summary from the local data for a property."""

    prop = data.get_property_by_id(property_id)
    if not prop:
        return {"error": f"Property with ID {property_id} not found"}
    area = prop.get("area", "")
    comps = data.get_sales_by_area(area)
    area_market = data.get_area_market_data(area)
    ppsf_values = [
        c["price_per_sqft"]
        for c in comps
        if isinstance(c.get("price_per_sqft"), (int, float))
    ]
    area_ppsf = round(sum(ppsf_values) / len(ppsf_values), 2) if ppsf_values else None
    sqft = prop.get("square_feet")
    estimate = round(area_ppsf * sqft, 2) if area_ppsf and sqft else None
    return {
        "property_id": property_id,
        "address": prop.get("address"),
        "area": area,
        "list_price": prop.get("price"),
        "square_feet": sqft,
        "bedrooms": prop.get("bedrooms"),
        "bathrooms": prop.get("bathrooms"),
        "comparable_count": len(comps),
        "area_avg_price_per_sqft": area_ppsf,
        "comparable_value_estimate": estimate,
        "area_market_data": area_market,
    }


def _heuristic_only_payload(
    property_id: str,
    heuristic: Dict[str, Any],
    *,
    note: str = _SAMPLING_UNAVAILABLE_NOTE,
    error: Optional[str] = None,
) -> str:
    payload = {
        "property_id": property_id,
        "heuristic_analysis": heuristic,
        "llm_reasoning": None,
        "note": note,
        "disclaimer": DISCLAIMER,
    }
    if error:
        payload["error"] = error
    return json.dumps(payload, indent=2)


def register_deep_analysis_tools(mcp: MCPServer) -> None:
    """Register deep property analysis tools with the MCP server."""

    data = get_data_manager()

    @mcp.tool()
    async def deep_analyze_property(
        property_id: str,
        focus: str = "overall value and investment potential",
        ctx: Context = None,
    ) -> str:
        """Analyze a property with data heuristics, then ask the client's LLM
        for deeper reasoning via MCP sampling. Falls back to heuristic-only
        output when the client does not support sampling. Not financial advice.
        """
        audit("deep_analyze_property", property_id=property_id, focus=focus)
        heuristic = _heuristic_summary(data, property_id)
        if "error" in heuristic:
            return json.dumps(heuristic, indent=2)

        supports_sampling = False
        if ctx is not None:
            try:
                supports_sampling = ctx.session.check_client_capability(
                    _SAMPLING_CAPABILITY
                )
            except ValueError:
                supports_sampling = False
        if not supports_sampling or ctx is None:
            return _heuristic_only_payload(property_id, heuristic)

        try:
            result = await ctx.session.create_message(
                messages=[
                    types.SamplingMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=(
                                f"Analyze this property with a focus on {focus}. "
                                f"Note anything the data summary may have missed in "
                                f"2-4 sentences.\n\n"
                                f"Property data:\n{json.dumps(heuristic, indent=2)}"
                            ),
                        ),
                    )
                ],
                max_tokens=500,
                system_prompt=(
                    "You are a careful real-estate analyst. Be specific and "
                    "concise. Not financial advice."
                ),
            )
            if result.content.type == "text":
                llm_text = result.content.text
            else:
                llm_text = str(result.content)
        except Exception as exc:
            return _heuristic_only_payload(
                property_id,
                heuristic,
                error=f"Sampling request failed: {exc}",
            )

        return json.dumps(
            {
                "property_id": property_id,
                "heuristic_analysis": heuristic,
                "llm_reasoning": llm_text,
                "disclaimer": DISCLAIMER,
            },
            indent=2,
        )
