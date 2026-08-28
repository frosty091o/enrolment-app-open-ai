import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent
AGENT_DIR = APP_DIR / "agentic_loop"
SERVICE_DIR = APP_DIR / "enrolment-service"
sys.path.insert(0, str(AGENT_DIR))
sys.path.insert(0, str(SERVICE_DIR))

from collectors import architecture_collector, db_collector
from core.prompt_registry import PromptRegistry
from pipelines import db_pipeline, endpoints_pipeline
from views.html_formatters import format_student_html, format_students_html
from routes.ai_mode import _context_answer_is_grounded


class Lab04StructureTests(unittest.TestCase):
    def test_required_prompt_families_resolve(self):
        registry = PromptRegistry(APP_DIR)
        self.assertIn(
            "PRECISION IMPLEMENTATION AGENT",
            registry.read("service", "implementation/system_prompt.txt"),
        )
        self.assertIn(
            "software architecture review assistant",
            registry.read("lab4", "implementation/architecture_system_prompt.txt"),
        )

    def test_database_collector_reads_preserved_lab3_data(self):
        ok, evidence = db_collector.collect(APP_DIR, APP_DIR)
        self.assertTrue(ok, evidence)
        self.assertIn("10 valid rows", evidence)
        self.assertIn("ASD101 rows count is 2", evidence)

    def test_architecture_collector_confirms_three_services(self):
        ok, evidence = architecture_collector.collect(APP_DIR, APP_DIR)
        self.assertTrue(ok, evidence)
        for service in ("frontend-service", "enrolment-service", "database-service"):
            self.assertIn(service, evidence)

    def test_pipeline_replaces_placeholders(self):
        registry = PromptRegistry(APP_DIR)
        task = registry.read("service", "implementation/task_prompt.txt")
        context = registry.read("service", "implementation/context_prompt.txt")
        output = db_pipeline.build_user_prompt(task, context, "10 valid rows")
        self.assertNotIn("{{REVIEW_TARGET}}", output)
        self.assertNotIn("{{VALIDATION_EVIDENCE}}", output)

    def test_passing_endpoint_evidence_uses_no_issue_gate(self):
        output = endpoints_pipeline.build_user_prompt(
            "{{REVIEW_TARGET}} {{VALIDATION_EVIDENCE}}",
            "context",
            "GET /students returned 200 in 4ms; POST /ask returned 200 in 20ms",
        )
        self.assertTrue(output.endswith("No evidence-backed improvement identified."))

    def test_html_formatters_escape_database_text(self):
        student = {
            "student_id": 1,
            "student_name": "<script>alert(1)</script>",
            "subject_code": "ASD101",
        }
        self.assertNotIn("<script>", format_student_html(student))
        self.assertNotIn("<script>", format_students_html([student]))

    def test_context_guard_rejects_invented_write_endpoints(self):
        self.assertFalse(
            _context_answer_is_grounded("Use POST /students to create a new student.")
        )
        self.assertTrue(
            _context_answer_is_grounded("GET /students returns the student list.")
        )


if __name__ == "__main__":
    unittest.main()
