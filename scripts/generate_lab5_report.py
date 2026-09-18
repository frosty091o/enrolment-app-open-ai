"""Generate Lab 5 reports from a real GitHub Actions run."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    required = ("GITHUB_RUN_ID", "GITHUB_SHA", "GITHUB_REF_NAME", "GITHUB_REPOSITORY")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise SystemExit("Cannot generate CI evidence without: " + ", ".join(missing))

    report = {
        "workflow_name": "lab5-ci",
        "run_id": os.environ["GITHUB_RUN_ID"],
        "commit_sha": os.environ["GITHUB_SHA"],
        "branch": os.environ["GITHUB_REF_NAME"],
        "generated_timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    run_url = (
        f"https://github.com/{os.environ['GITHUB_REPOSITORY']}"
        f"/actions/runs/{report['run_id']}"
    )
    reports = Path(__file__).resolve().parent.parent / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    (reports / "report.md").write_text(
        "# Lab 05 Workflow Report\n\n"
        f"- Workflow: {report['workflow_name']}\n"
        f"- Run ID: {report['run_id']}\n"
        f"- Commit SHA: {report['commit_sha']}\n"
        f"- Branch: {report['branch']}\n"
        f"- Generated: {report['generated_timestamp']}\n",
        encoding="utf-8",
    )
    (reports / "run-view.md").write_text(f"Run URL: {run_url}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
