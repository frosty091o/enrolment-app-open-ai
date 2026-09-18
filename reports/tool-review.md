# Lab 7 MCP Tool Review

## Risks and corrections

- **Path exposure:** A user-controlled directory could point outside the project. `project_files` resolves the requested path and rejects traversal or paths outside the root. It also hides `.env`, `.git`, Python environments, and bytecode directories. The Flask route rejects absolute and parent-traversal paths before calling MCP.
- **CI scope:** `ci_report` accepts only `reports/report.json` and returns its contents. It does not grant release approval. The Flask route rejects other report paths.
- **Input errors:** Empty subject codes are rejected by the Flask route and tool. The server has no write tools.
- **Local access:** The MCP HTTP host port is bound to loopback; containers access it on the private Compose network. Authentication and audit logging remain future work if the service is deployed beyond a local lab.

## Retest and human decision

Unit tests passed for student data, empty results, excluded names, traversal, and report restriction. Live MCP protocol calls returned 10 students, two ASD101 rows, project names, and Lab 5 run metadata. The browser-facing route returned HTTP 403 when the switch header was absent and HTTP 200 when enabled. A review-model suggestion that `ci_report` should decide release approval was rejected because it violated the tool boundary; the review prompt was tightened and rerun. **Decision: accept the implementation and retain read-only CI metadata.**
