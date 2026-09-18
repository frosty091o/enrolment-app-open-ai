import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR / "agentic_loop"))
sys.path.insert(0, str(APP_DIR / "scripts"))

from collectors import devops_collector
import generate_lab5_report


class Lab05EvidenceTests(unittest.TestCase):
    def test_report_generator_and_collector_agree_on_run(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            workflow = root / ".github" / "workflows" / "lab5-ci.yml"
            workflow.parent.mkdir(parents=True)
            shutil.copyfile(APP_DIR / ".github" / "workflows" / "lab5-ci.yml", workflow)
            script_path = root / "scripts" / "generate_lab5_report.py"
            environment = {
                "GITHUB_RUN_ID": "123456",
                "GITHUB_SHA": "a" * 40,
                "GITHUB_REF_NAME": "main",
                "GITHUB_REPOSITORY": "example/enrolment-app-open-ai",
            }
            with patch.object(generate_lab5_report, "__file__", str(script_path)):
                with patch.dict(os.environ, environment):
                    generate_lab5_report.main()

            report = json.loads((root / "reports" / "report.json").read_text())
            self.assertEqual(report["run_id"], "123456")
            self.assertEqual(report["branch"], "main")
            ok, evidence = devops_collector.collect(root, root)
            self.assertTrue(ok, evidence)
            self.assertIn("run 123456", evidence)

            (root / "reports" / "run-view.md").write_text("Run URL: placeholder\n")
            ok, error = devops_collector.collect(root, root)
            self.assertFalse(ok)
            self.assertIn("matching report.json run_id", error)

    def test_missing_reports_do_not_pass_review_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            workflow = root / ".github" / "workflows" / "lab5-ci.yml"
            workflow.parent.mkdir(parents=True)
            shutil.copyfile(APP_DIR / ".github" / "workflows" / "lab5-ci.yml", workflow)
            ok, error = devops_collector.collect(root, root)
            self.assertFalse(ok)
            self.assertIn("Download the lab5-report artifact", error)


if __name__ == "__main__":
    unittest.main()
