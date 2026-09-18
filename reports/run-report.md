# Lab 7 MCP Run Report

Run date: 18 September 2026. Environment: Docker Compose, MCP Python SDK 2.2.0, Ollama Qwen 2.5 0.5B and Llama 3.1 8B.

## Terminal results

`docker compose ps` showed `database-service`, `enrolment-service`, `frontend-service`, and `mcp-server` running. The MCP server advertised `student_count`, `students_by_subject`, `project_files`, and `ci_report`.

| Live MCP call | Observed output |
| --- | --- |
| `student_count` | `{"student_count": 10}` |
| `students_by_subject({"subject_code":"ASD101"})` | Two rows: John Smith and Sarah Jones |
| `project_files({"directory_path":"."})` | 25 project entries, including `mcp-server`, `prompts`, and `reports`; `.env` excluded |
| `ci_report({"report_path":"reports/report.json"})` | `workflow_name=lab5-ci`, `run_id=35310145492`, `branch=main` |

The Flask MCP endpoints returned HTTP 200 for all four valid calls. Without `X-MCP-Mode: on`, `student-count` returned HTTP 403. The boundary tests reject path traversal and other report paths. The test suite returned `Ran 12 tests ... OK`.

[GitHub Actions run 35310145492](https://github.com/frosty091o/enrolment-app-open-ai/actions/runs/35310145492) passed `build-images`, `smoke-check` (including the MCP-backed student count), and `evidence-pack` on commit `fe8b33df8378590bed459ffea301a40e291d8e61`. Its `lab5-report` artifact was downloaded into `reports/report.json`, `report.md`, and `run-view.md`.

## Browser verification

At `http://localhost:8080/#mcp` in Chrome, MCP Mode initially displayed OFF with disabled tool buttons. Switching it ON enabled the buttons. The four result panels visibly displayed the same student count, ASD101 rows, project entries, and CI metadata as the protocol calls. Browser inspection was performed during this run; no screenshot file was saved.

## Agentic workflow

`printf '4\\n5\\n0\\n' | .venv-lab7/bin/python agentic_loop.py` reached START, OBSERVE, PROMPTS, LLM implementation, LLM review, and DONE for both DevOps and MCP. DevOps OBSERVE confirmed the new CI run and all three jobs. MCP OBSERVE contained results from all four actual tool calls. The implementation model selected the matching tools and echoed their observed values. The final review concluded: "Each tool's boundary is respected ... No tool is granted permission to edit files, enrolments, or CI runs ... conclusions follow from the results." See `tool-review.md` for the rejected CI approval suggestion and prompt correction.
