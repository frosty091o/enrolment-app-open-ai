"""Boundary and evidence checks for the Lab 7 read-only tools."""

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("lab7_tools", ROOT / "mcp-server" / "tools.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


class Lab7ToolTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name).resolve()
        connection = sqlite3.connect(self.root / "enrolment.db")
        connection.execute("CREATE TABLE students (student_id INTEGER, student_name TEXT, subject_code TEXT)")
        connection.executemany("INSERT INTO students VALUES (?, ?, ?)", [
            (1, "John Smith", "ASD101"), (2, "Sarah Jones", "ASD101"),
            (3, "Pat Lee", "DB102"),
        ])
        connection.commit()
        connection.close()
        (self.root / "reports").mkdir()
        (self.root / "reports" / "report.json").write_text(json.dumps({"workflow_name": "lab5-ci"}))
        (self.root / ".env").write_text("secret=test")
        self.project_patch = patch.object(tools, "PROJECT_ROOT", self.root)
        self.database_patch = patch.object(tools, "DATABASE_PATH", self.root / "enrolment.db")
        self.service_patch = patch.object(tools, "DATABASE_SERVICE_URL", None)
        for mocked in (self.project_patch, self.database_patch, self.service_patch):
            mocked.start()

    def tearDown(self):
        for mocked in (self.project_patch, self.database_patch, self.service_patch):
            mocked.stop()
        self.folder.cleanup()

    def test_student_tools_return_existing_rows(self):
        self.assertEqual(tools.get_student_count(), {"student_count": 3})
        rows = tools.get_students_by_subject("asd101")
        self.assertEqual([row["student_id"] for row in rows], [1, 2])
        self.assertEqual(tools.get_students_by_subject("MISSING"), [])

    def test_file_and_report_tools_stay_inside_boundaries(self):
        entries = tools.list_project_files(".")
        self.assertIn("reports", entries)
        self.assertNotIn(".env", entries)
        with self.assertRaises(ValueError):
            tools.list_project_files("../../")
        with self.assertRaises(ValueError):
            tools.list_project_files(".env")
        (self.root / "outside-link").symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            tools.list_project_files("outside-link")
        self.assertEqual(tools.read_ci_report()["workflow_name"], "lab5-ci")
        with self.assertRaises(ValueError):
            tools.read_ci_report(".env")


if __name__ == "__main__":
    unittest.main()
