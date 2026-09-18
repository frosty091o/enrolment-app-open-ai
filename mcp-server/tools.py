"""Read-only data access behind the Lab 7 MCP tools."""

import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.getenv("MCP_PROJECT_ROOT", str(BASE_DIR.parent))).resolve()
DATABASE_PATH = PROJECT_ROOT / "enrolment.db"
DATABASE_SERVICE_URL = os.getenv("DATABASE_SERVICE_URL")
EXCLUDED_NAMES = {".env", ".git", ".venv", ".venv-lab7", "__pycache__"}


def _connect_db():
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(f"Student database not found: {DATABASE_PATH}")
    connection = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def get_student_count() -> dict:
    """Count existing student records; do not modify enrolments."""
    if DATABASE_SERVICE_URL:
        response = requests.get(f"{DATABASE_SERVICE_URL}/students", timeout=5)
        response.raise_for_status()
        return {"student_count": len(response.json())}
    with closing(_connect_db()) as connection:
        row = connection.execute("SELECT COUNT(*) FROM students").fetchone()
        return {"student_count": row[0]}


def get_students_by_subject(subject_code: str) -> list:
    """Return enrolments for one subject code; do not infer student performance."""
    subject = (subject_code or "").strip().upper()
    if not subject:
        raise ValueError("subject_code is required")
    if DATABASE_SERVICE_URL:
        response = requests.get(
            f"{DATABASE_SERVICE_URL}/students/by-subject",
            params={"subject_code": subject},
            timeout=5,
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()
    with closing(_connect_db()) as connection:
        rows = connection.execute(
            "SELECT student_id, student_name, subject_code FROM students "
            "WHERE subject_code = ? ORDER BY student_id",
            (subject,),
        ).fetchall()
        return [dict(row) for row in rows]


def list_project_files(directory_path: str = ".") -> list:
    """List names in a project directory; never read file contents."""
    requested = (directory_path or ".").strip()
    if requested == "..":  # Accept the path used by the lab's examples.
        requested = "."
    path = (PROJECT_ROOT / requested).resolve()
    if path != PROJECT_ROOT and PROJECT_ROOT not in path.parents:
        raise ValueError("directory_path must stay inside the project")
    relative_parts = path.relative_to(PROJECT_ROOT).parts
    if any(part in EXCLUDED_NAMES for part in relative_parts):
        raise ValueError("directory_path is not available to this tool")
    if not path.is_dir():
        raise FileNotFoundError(f"Project directory not found: {requested}")
    return sorted(item.name for item in path.iterdir() if item.name not in EXCLUDED_NAMES)


def read_ci_report(report_path: str = "reports/report.json") -> dict:
    """Read the Lab 5 JSON report; do not decide release approval."""
    if report_path not in {"reports/report.json", "../reports/report.json"}:
        raise ValueError("Only reports/report.json is available to this tool")
    path = PROJECT_ROOT / "reports" / "report.json"
    if not path.is_file():
        raise FileNotFoundError("Lab 5 report missing: run lab5-ci and download lab5-report")
    with path.open(encoding="utf-8") as source:
        return json.load(source)
