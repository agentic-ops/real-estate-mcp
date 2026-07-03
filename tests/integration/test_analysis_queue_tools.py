"""Integration tests for the async property-analysis queue."""

import pytest

import tools.analysis_queue_tools as queue_module
from tests.conftest import call_tool_json

SAMPLE_LISTING = """Charming Townhouse
Address: 12 Maple Court
Price: $410,000
3 bedrooms, 2 bathrooms
1,800 sq ft
"""


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Point the queue at a throwaway SQLite database for each test."""

    monkeypatch.setattr(queue_module, "_DB_PATH", tmp_path / "queue.db")


@pytest.fixture
def listing_file(tmp_path):
    path = tmp_path / "listing.txt"
    path.write_text(SAMPLE_LISTING, encoding="utf-8")
    return str(path)


class TestAnalysisQueue:
    async def test_queue_and_retrieve(self, mcp_server, listing_file):
        queued = await call_tool_json(
            mcp_server,
            "queue_property_analysis",
            {"file_path": listing_file, "analysis_notes": "test"},
        )
        assert queued["status"] == "complete"
        job_id = queued["job_id"]

        status = await call_tool_json(
            mcp_server, "get_analysis_status", {"job_id": job_id}
        )
        assert status["status"] == "complete"
        assert status["analysis_notes"] == "test"

        result = await call_tool_json(
            mcp_server, "get_analysis_result", {"job_id": job_id}
        )
        assert result["extracted_fields"]["price"] == 410000.0
        assert result["price_per_sqft"] is not None

    async def test_queue_missing_file(self, mcp_server):
        queued = await call_tool_json(
            mcp_server, "queue_property_analysis", {"file_path": "/no/such.txt"}
        )
        assert queued["status"] == "error"

    async def test_status_unknown_job(self, mcp_server):
        result = await call_tool_json(
            mcp_server, "get_analysis_status", {"job_id": "unknown"}
        )
        assert "error" in result

    async def test_list_jobs(self, mcp_server, listing_file):
        await call_tool_json(
            mcp_server, "queue_property_analysis", {"file_path": listing_file}
        )
        listed = await call_tool_json(mcp_server, "list_analysis_jobs", {})
        assert listed["job_count"] >= 1
        assert len(listed["jobs"]) == listed["job_count"]
