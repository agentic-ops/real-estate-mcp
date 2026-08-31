"""Async local property-analysis queue.

Provides a persistent SQLite-backed job queue for analyzing listing
documents. Jobs are queued, run inline (synchronously), and results are
stored for retrieval. This is a local analysis store -- not a submission
service to any external system.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Optional, Tuple

from mcp.server.mcpserver import MCPServer

from utils import audit

_DB_PATH = Path("real_estate_mcp_analysis.db")


def _db_path() -> Path:
    """Return the database path (overridable in tests via module attribute)."""
    return _DB_PATH


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_jobs (
            job_id      TEXT PRIMARY KEY,
            file_path   TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'queued',
            analysis_notes TEXT NOT NULL DEFAULT '',
            result      TEXT,
            error       TEXT,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
        """)
    conn.commit()


@contextmanager
def _get_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(str(_db_path()))
    conn.row_factory = sqlite3.Row
    _init_db(conn)
    try:
        yield conn
    finally:
        conn.close()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run_analysis(file_path: str) -> Tuple[Optional[str], Optional[str]]:
    """Run listing extraction and return (result_json, error_str)."""
    from tools.document_tools import extract_listing_fields, read_listing_text

    try:
        text = read_listing_text(file_path)
    except FileNotFoundError:
        return None, "File not found."
    except ValueError as exc:
        return None, str(exc)

    fields = extract_listing_fields(text)
    price = fields.get("price")
    sqft = fields.get("square_feet")
    price_per_sqft = round(price / sqft, 2) if price and sqft else None
    result = {
        "file_path": file_path,
        "title": Path(file_path).name,
        "extracted_fields": fields,
        "price_per_sqft": price_per_sqft,
        "notice": "Automated extraction for review; verify against source listing.",
    }
    return json.dumps(result, indent=2), None


def register_analysis_queue_tools(mcp: MCPServer) -> None:
    """Register async property-analysis queue tools with the MCP server."""

    @mcp.tool()
    def queue_property_analysis(file_path: str, analysis_notes: str = "") -> str:
        """Queue a listing document for analysis. Returns a job ID immediately.

        Runs listing extraction and persists the result. Use
        get_analysis_status and get_analysis_result to retrieve it.
        """
        audit("queue_property_analysis", file_path=file_path)
        job_id = str(uuid.uuid4())
        now = _now_iso()
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO analysis_jobs (job_id, file_path, status, "
                "analysis_notes, created_at, updated_at) "
                "VALUES (?, ?, 'queued', ?, ?, ?)",
                (job_id, file_path, analysis_notes, now, now),
            )
            conn.commit()

        result_json, error = _run_analysis(file_path)
        updated = _now_iso()
        with _get_conn() as conn:
            if error:
                conn.execute(
                    "UPDATE analysis_jobs SET status='error', error=?, "
                    "updated_at=? WHERE job_id=?",
                    (error, updated, job_id),
                )
            else:
                conn.execute(
                    "UPDATE analysis_jobs SET status='complete', result=?, "
                    "updated_at=? WHERE job_id=?",
                    (result_json, updated, job_id),
                )
            conn.commit()

        return json.dumps(
            {
                "job_id": job_id,
                "file_path": file_path,
                "status": "error" if error else "complete",
                "message": (
                    error
                    if error
                    else "Analysis complete. Use get_analysis_result to retrieve it."
                ),
            },
            indent=2,
        )

    @mcp.tool()
    def get_analysis_status(job_id: str) -> str:
        """Check the status of a queued analysis job (queued/complete/error)."""
        audit("get_analysis_status", job_id=job_id)
        with _get_conn() as conn:
            row = conn.execute(
                "SELECT job_id, file_path, status, analysis_notes, created_at, "
                "updated_at, error FROM analysis_jobs WHERE job_id=?",
                (job_id,),
            ).fetchone()
        if row is None:
            return json.dumps({"job_id": job_id, "error": "Job not found."}, indent=2)
        return json.dumps(
            {
                "job_id": row["job_id"],
                "file_path": row["file_path"],
                "status": row["status"],
                "analysis_notes": row["analysis_notes"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "error": row["error"],
            },
            indent=2,
        )

    @mcp.tool()
    def get_analysis_result(job_id: str) -> str:
        """Retrieve the completed analysis result for a queued job."""
        audit("get_analysis_result", job_id=job_id)
        with _get_conn() as conn:
            row = conn.execute(
                "SELECT job_id, status, result, error FROM analysis_jobs "
                "WHERE job_id=?",
                (job_id,),
            ).fetchone()
        if row is None:
            return json.dumps({"job_id": job_id, "error": "Job not found."}, indent=2)
        if row["status"] == "error":
            return json.dumps(
                {"job_id": job_id, "status": "error", "error": row["error"]}, indent=2
            )
        if row["status"] != "complete":
            return json.dumps(
                {
                    "job_id": job_id,
                    "status": row["status"],
                    "message": "Analysis not yet complete.",
                },
                indent=2,
            )
        raw_result = row["result"]
        try:
            parsed = json.loads(raw_result) if raw_result else {}
        except (json.JSONDecodeError, TypeError):
            parsed = {"raw": raw_result}
        parsed["job_id"] = job_id
        return json.dumps(parsed, indent=2)

    @mcp.tool()
    def list_analysis_jobs() -> str:
        """List all queued analysis jobs with their statuses and timestamps."""
        audit("list_analysis_jobs")
        with _get_conn() as conn:
            rows = conn.execute(
                "SELECT job_id, file_path, status, analysis_notes, created_at, "
                "updated_at FROM analysis_jobs ORDER BY created_at DESC"
            ).fetchall()
        jobs = [
            {
                "job_id": row["job_id"],
                "file_path": row["file_path"],
                "status": row["status"],
                "analysis_notes": row["analysis_notes"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]
        return json.dumps({"job_count": len(jobs), "jobs": jobs}, indent=2)
