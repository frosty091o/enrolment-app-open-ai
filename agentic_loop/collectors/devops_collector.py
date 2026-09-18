"""Collect local workflow structure and downloaded GitHub Actions evidence."""

import json
import re
from pathlib import Path


REQUIRED_JOBS = ("build-images", "smoke-check", "evidence-pack")
REQUIRED_KEYS = (
    "workflow_name", "run_id", "commit_sha", "branch", "generated_timestamp"
)


def collect(app_dir: Path, repo_root: Path):
    workflow = repo_root / ".github" / "workflows" / "lab5-ci.yml"
    if not workflow.is_file():
        return False, "Missing .github/workflows/lab5-ci.yml"

    content = workflow.read_text(encoding="utf-8")
    checks = {
        "manual workflow_dispatch trigger": bool(re.search(r"(?m)^  workflow_dispatch:", content)),
        "build-images job": bool(re.search(r"(?m)^  build-images:", content)),
        "smoke-check job": bool(re.search(r"(?m)^  smoke-check:", content)),
        "evidence-pack job": bool(re.search(r"(?m)^  evidence-pack:", content)),
        "build before smoke": "needs: [build-images]" in content,
        "smoke before evidence": "needs: [smoke-check]" in content,
        "all three HTTP smoke checks": all(
            f"http://localhost:{port}/" in content for port in (8080, 5001, 5002)
        ),
        "always-run volume cleanup": "if: always()" in content and "docker compose down -v" in content,
        "lab5-report artifact upload": "actions/upload-artifact@v4" in content and "name: lab5-report" in content,
    }
    failed = [label for label, passed in checks.items() if not passed]
    if failed:
        return False, "Workflow checks failed: " + ", ".join(failed)

    reports = app_dir / "reports"
    paths = [reports / name for name in ("report.json", "report.md", "run-view.md")]
    missing = [str(path.relative_to(app_dir)) for path in paths if not path.is_file()]
    if missing:
        return False, "Download the lab5-report artifact first. Missing: " + ", ".join(missing)

    try:
        report = json.loads(paths[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"Invalid reports/report.json: {exc}"
    missing_keys = [key for key in REQUIRED_KEYS if not report.get(key)]
    if missing_keys:
        return False, "report.json missing values: " + ", ".join(missing_keys)
    if report["workflow_name"] != "lab5-ci":
        return False, "report.json workflow_name is not lab5-ci"

    summary = paths[1].read_text(encoding="utf-8")
    if not all(str(report[key]) in summary for key in ("workflow_name", "run_id", "commit_sha", "branch")):
        return False, "report.md does not match report.json run metadata"

    run_view = paths[2].read_text(encoding="utf-8")
    url_pattern = rf"https://github\.com/[^/\s]+/[^/\s]+/actions/runs/{re.escape(str(report['run_id']))}\b"
    if not re.search(url_pattern, run_view):
        return False, "run-view.md has no GitHub Actions URL matching report.json run_id"

    return True, (
        "Workflow: manual lab5-ci; build-images -> smoke-check -> evidence-pack; "
        "smoke targets 8080, 5001, 5002; always-run docker compose down -v; "
        "lab5-report artifact upload configured. "
        f"Downloaded report: run {report['run_id']}, commit {report['commit_sha']}, "
        f"branch {report['branch']}, generated {report['generated_timestamp']}; "
        "report.md and run-view.md match. "
        "Local files do not independently prove GitHub job success or artifact upload."
    )
