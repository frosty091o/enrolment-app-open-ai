"""Browser-facing routes that invoke the real Lab 7 MCP server."""

import asyncio
import html
import json
import os
from pathlib import PurePosixPath

from flask import Blueprint, request
from mcp import Client


mcp_mode_bp = Blueprint("mcp_mode", __name__, url_prefix="/mcp")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


def _enabled():
    return os.getenv("MCP_ENABLED", "true").lower() == "true" and request.headers.get("X-MCP-Mode") == "on"


async def _invoke(tool_name: str, arguments: dict):
    async with Client(MCP_SERVER_URL) as client:
        result = await client.call_tool(tool_name, arguments)
        if result.is_error:
            raise ValueError("; ".join(block.text for block in result.content if hasattr(block, "text")))
        if result.structured_content is not None:
            return result.structured_content
        items = []
        for block in result.content:
            if hasattr(block, "text"):
                try:
                    items.append(json.loads(block.text))
                except json.JSONDecodeError:
                    items.append(block.text)
        return items[0] if tool_name in {"student_count", "ci_report"} and len(items) == 1 else items


def _call(tool_name: str, arguments: dict):
    if not _enabled():
        return "<p>MCP Mode is off.</p>", 403
    try:
        data = asyncio.run(_invoke(tool_name, arguments))
        rendered = html.escape(json.dumps(data, indent=2, ensure_ascii=False))
        return f"<pre>{rendered}</pre>", 200
    except ValueError as exc:
        return f"<p>{html.escape(str(exc))}</p>", 400
    except Exception as exc:
        return f"<p>MCP server unavailable: {html.escape(str(exc))}</p>", 503


@mcp_mode_bp.get("/student-count")
def student_count():
    return _call("student_count", {})


@mcp_mode_bp.get("/students-by-subject")
def students_by_subject():
    subject_code = request.args.get("subject_code", "").strip().upper()
    if not subject_code:
        return "<p>Subject code is required.</p>", 400
    return _call("students_by_subject", {"subject_code": subject_code})


@mcp_mode_bp.get("/project-files")
def project_files():
    directory_path = request.args.get("directory_path", ".").strip() or "."
    path = PurePosixPath(directory_path)
    if path.is_absolute() or ".." in path.parts:
        return "<p>Project directory must stay within the project.</p>", 400
    return _call("project_files", {"directory_path": directory_path})


@mcp_mode_bp.get("/ci-report")
def ci_report():
    report_path = request.args.get("report_path", "reports/report.json")
    if report_path != "reports/report.json":
        return "<p>Only reports/report.json is available.</p>", 400
    return _call("ci_report", {"report_path": report_path})
