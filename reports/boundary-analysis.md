# Lab 7 MCP Tool Boundary Analysis

| Tool | Permitted responsibility | Outside its boundary |
| --- | --- | --- |
| `student_count` | Count existing student rows through the database API | Change enrolments or interpret policy |
| `students_by_subject` | Return existing rows for one supplied subject code | Predict performance or edit rows |
| `project_files` | List file and folder names inside the project | Read contents, expose excluded names, traverse outside the project |
| `ci_report` | Read `reports/report.json` | Trigger CI or decide release approval |

Decision: **Accepted for this local lab environment.** The server exposes read-only tools; the browser routes invoke the server through MCP. The project tool resolves and checks paths against the project root, and the CI tool accepts only the Lab 5 JSON report. The host port is bound to `127.0.0.1`. There is no user authentication on the local MCP endpoint, so it must not be exposed to an untrusted network without an access layer.
