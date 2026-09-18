"""Collect real MCP tool results for Lab 7 review."""

import asyncio
import json
import os
from pathlib import Path

REQUIRED_TOOLS = {"student_count", "students_by_subject", "project_files", "ci_report"}
REQUIRED_FILES = (
    "mcp-server/server.py", "mcp-server/tools.py", "mcp-server/requirements.txt",
    "frontend-service/templates/tabs/mcp.html", "enrolment-service/routes/mcp_mode.py",
    "prompts/lab7/implementation/tool_selection_prompt.txt",
    "prompts/lab7/review/integration_review_prompt.txt",
    "prompts/lab7/review/tool_review_prompt.txt", "reports/report.json",
)


async def _collect(url):
    from mcp import Client

    async with Client(url) as client:
        found = {tool.name for tool in (await client.list_tools()).tools}
        missing = REQUIRED_TOOLS - found
        if missing:
            raise ValueError("MCP server missing tools: " + ", ".join(sorted(missing)))
        evidence = {}
        for name, arguments in (
            ("student_count", {}),
            ("students_by_subject", {"subject_code": "ASD101"}),
            ("project_files", {"directory_path": "."}),
            ("ci_report", {"report_path": "reports/report.json"}),
        ):
            result = await client.call_tool(name, arguments)
            if result.is_error:
                raise ValueError(f"{name} failed: {result.content}")
            if result.structured_content is not None:
                evidence[name] = result.structured_content
            else:
                items = []
                for block in result.content:
                    if hasattr(block, "text"):
                        try:
                            items.append(json.loads(block.text))
                        except json.JSONDecodeError:
                            items.append(block.text)
                evidence[name] = items[0] if name in {"student_count", "ci_report"} and len(items) == 1 else items
            if not evidence[name] and name != "students_by_subject":
                raise ValueError(f"{name} returned no evidence")
        return evidence


def collect(app_dir: Path, repo_root: Path):
    missing = [name for name in REQUIRED_FILES if not (repo_root / name).is_file()]
    if missing:
        return False, "Missing Lab 7 files: " + ", ".join(missing)
    url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")
    try:
        results = asyncio.run(_collect(url))
    except Exception as exc:
        return False, f"MCP invocation failed at {url}: {exc}"
    return True, "MCP server listed and executed all four tools: " + json.dumps(results, sort_keys=True)
