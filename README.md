# Student Enrolment App — Labs 04–05 and 07

This project refactors the Lab 03 Flask monolith into a containerized application with Normal UI, AI Mode, and Lab 07 MCP Mode flows.

## Architecture

```text
Browser -> frontend-service:8080 -> enrolment-service:5001 -> database-service:5002 -> SQLite
                                      |
                                      +-> Ollama on the host
                                      +-> mcp-server:8000 -> database-service and read-only project files
```

- `frontend-service`: Nginx, HTML, CSS, tabs, forms, and browser interaction.
- `enrolment-service`: Flask routes, validation, formatting, prompt loading, database API integration, and Ollama calls.
- `database-service`: SQLite initialization, persistence, and JSON data APIs.
- `agentic_loop`: modular DB, endpoint, architecture, and DevOps evidence reviews.
- `mcp-server`: four read-only Model Context Protocol tools for enrolments, project entries, and Lab 5 CI evidence.
- `legacy-lab3`: preserved Lab 03 application.

See [ADR-001](architecture/ADR-001-three-service-architecture.md) and the [service-boundary record](architecture/service-boundaries.md).

## Run in VS Code

Docker Desktop and Ollama must be running. Start the application from the repository root:

```bash
docker compose up --build -d
docker compose ps
```

Open <http://localhost:8080>. The Flask API is available at <http://localhost:5001> and the database API at <http://localhost:5002>.

Run the modular review loop:

```bash
.venv/bin/python agentic_loop.py
```

For Lab 07, create a Python 3.11+ environment and install both sets of dependencies:

```bash
python3.11 -m venv .venv-lab7
.venv-lab7/bin/pip install -r requirements.txt -r mcp-server/requirements.txt
.venv-lab7/bin/python agentic_loop.py
```

Choose **5 - MCP** to list and invoke all four tools, then run the two-model review. **6 - Run All** includes MCP. The web tab at <http://localhost:8080/#mcp> has an ON/OFF switch and controls for each tool. The MCP server is reachable from the host only at `http://localhost:8000/mcp`; the browser calls Flask, which invokes the MCP protocol. Student and subject tools read the database API, the file tool lists names within this project, and the CI tool reads only `reports/report.json`. The CI report contains run metadata; it is not a release decision.

## Lab 05 CI

The manual [Lab 5 workflow](.github/workflows/lab5-ci.yml) builds the application images,
images, starts the services, checks HTTP 200 on ports 8080, 5001, and 5002,
stops containers and volumes, then uploads the `lab5-report` artifact. The
workflow runs from this repository root.

Push the workflow to `main`, open GitHub **Actions → lab5-ci → Run workflow**,
select `main`, and wait for the three jobs to pass. Download `lab5-report` and
extract `report.json`, `report.md`, and `run-view.md` into `reports/`.
Run `.venv/bin/python agentic_loop.py` and choose **4 - DevOps** to review the
downloaded evidence. A missing artifact is reported as missing rather than
treated as a successful run.

Run local structural tests:

```bash
.venv-lab7/bin/python -m unittest discover -s tests -v
```

Stop the application:

```bash
docker compose down
```

See [evidence_log.md](evidence_log.md) for endpoint results, NFR timing, prompt-improvement comparisons, and reflections.
