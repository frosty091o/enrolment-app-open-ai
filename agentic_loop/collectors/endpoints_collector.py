import os
import re
from pathlib import Path

import requests


ROUTE_PATTERN = re.compile(r'@\w+_bp\.(get|post)\("([^"]+)"\)')


def _request_details(method: str, path: str):
    if method == "get" and path == "/students/by-id":
        return {"params": {"student_id": "1"}, "timeout": 5}
    if method == "get" and path == "/students/by-subject":
        return {"params": {"subject_code": "ASD101"}, "timeout": 5}
    if method == "post" and path in {"/ask", "/ask-with-context"}:
        return {"data": {"question": "Explain the app briefly."}, "timeout": 180}
    if method == "post":
        return {
            "data": {
                "architecture_request": (
                    "Review the three service boundaries using supplied evidence."
                )
            },
            "timeout": 180,
        }
    return {"timeout": 5}


def _test_endpoint(base_url: str, method: str, path: str) -> str:
    try:
        response = requests.request(
            method.upper(), f"{base_url}{path}", **_request_details(method, path)
        )
        elapsed_ms = int(response.elapsed.total_seconds() * 1000)
        return f"{method.upper()} {path} returned {response.status_code} in {elapsed_ms}ms"
    except requests.ConnectionError:
        return f"{method.upper()} {path} [CONNECTION REFUSED - app not running]"
    except requests.Timeout:
        return f"{method.upper()} {path} [TIMEOUT]"
    except Exception as exc:
        return f"{method.upper()} {path} [ERROR: {type(exc).__name__}]"


def collect(app_dir: Path, repo_root: Path):
    base_url = os.getenv("FLASK_BASE_URL", "http://localhost:5001")
    route_files = [
        app_dir / "enrolment-service" / "routes" / "normal_ui.py",
        app_dir / "enrolment-service" / "routes" / "ai_mode.py",
    ]
    missing = [str(path.relative_to(app_dir)) for path in route_files if not path.exists()]
    if missing:
        return False, "Missing route files: " + ", ".join(missing)

    endpoints = []
    for route_file in route_files:
        endpoints.extend(ROUTE_PATTERN.findall(route_file.read_text(encoding="utf-8")))
    if not endpoints:
        return False, "No Flask routes found in route files."

    results = [_test_endpoint(base_url, method, route) for method, route in sorted(set(endpoints))]
    if results and all("CONNECTION REFUSED" in result for result in results):
        return False, "Flask app not running. Start the app first, then run the agentic loop."
    return True, "Live endpoint evidence: " + "; ".join(results) + "."
