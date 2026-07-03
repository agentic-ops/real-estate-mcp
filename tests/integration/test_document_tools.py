"""Integration tests for listing-document ingestion and export tools."""

import json

from tests.conftest import call_tool_json
from tools.document_tools import extract_listing_fields

SAMPLE_LISTING = """Beautiful Single Family Home
Address: 742 Evergreen Terrace, Riverside
Price: $625,000
4 bedrooms, 3 bathrooms
2,450 sq ft
Year built: 2005
Features: Pool, Garage, Updated Kitchen
"""


def _write_txt(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


class TestExtraction:
    def test_extract_fields(self):
        fields = extract_listing_fields(SAMPLE_LISTING)
        assert fields["price"] == 625000.0
        assert fields["bedrooms"] == 4.0
        assert fields["bathrooms"] == 3.0
        assert fields["square_feet"] == 2450
        assert fields["year_built"] == 2005
        assert fields["property_type"] == "Single Family Home"
        assert "742 Evergreen Terrace" in fields["address"]

    def test_extract_partial(self):
        fields = extract_listing_fields("A cozy condo priced at $300,000.")
        assert fields["price"] == 300000.0
        assert fields["property_type"] == "Condo"
        assert fields["bedrooms"] is None


class TestDocumentTools:
    async def test_ingest_listing_document(self, mcp_server, tmp_path):
        path = _write_txt(tmp_path, "listing.txt", SAMPLE_LISTING)
        result = await call_tool_json(
            mcp_server, "ingest_listing_document", {"file_path": path}
        )
        assert result["extracted_fields"]["price"] == 625000.0

    async def test_ingest_missing_file(self, mcp_server):
        result = await call_tool_json(
            mcp_server, "ingest_listing_document", {"file_path": "/no/such.txt"}
        )
        assert "error" in result

    async def test_ingest_unsupported_format(self, mcp_server, tmp_path):
        path = _write_txt(tmp_path, "listing.csv", "price,beds\n1,2")
        result = await call_tool_json(
            mcp_server, "ingest_listing_document", {"file_path": path}
        )
        assert "error" in result

    async def test_compare_listing_documents(self, mcp_server, tmp_path):
        a = _write_txt(tmp_path, "a.txt", SAMPLE_LISTING)
        b = _write_txt(
            tmp_path,
            "b.txt",
            SAMPLE_LISTING.replace("$625,000", "$700,000").replace(
                "4 bedrooms", "5 bedrooms"
            ),
        )
        result = await call_tool_json(
            mcp_server,
            "compare_listing_documents",
            {"file_path_a": a, "file_path_b": b},
        )
        assert result["difference_count"] >= 2
        assert "price" in result["differences"]

    async def test_export_property_report_docx(self, mcp_server, tmp_path):
        ingest = await call_tool_json(
            mcp_server,
            "ingest_listing_document",
            {"file_path": _write_txt(tmp_path, "listing.txt", SAMPLE_LISTING)},
        )
        out = tmp_path / "report.docx"
        result = await call_tool_json(
            mcp_server,
            "export_property_report",
            {"report_json": json.dumps(ingest), "output_path": str(out)},
        )
        assert out.exists()
        assert result["output_path"].endswith(".docx")

    async def test_export_requires_docx_extension(self, mcp_server, tmp_path):
        result = await call_tool_json(
            mcp_server,
            "export_property_report",
            {"report_json": "{}", "output_path": str(tmp_path / "report.pdf")},
        )
        assert "error" in result

    async def test_export_invalid_json(self, mcp_server, tmp_path):
        result = await call_tool_json(
            mcp_server,
            "export_property_report",
            {"report_json": "not json", "output_path": str(tmp_path / "r.docx")},
        )
        assert "error" in result
