# Student Enrolment App — Labs 04–05

This project refactors the Lab 03 Flask monolith into a containerized three-service architecture with separate Normal UI and AI Mode flows.

## Architecture

```text
Browser -> frontend-service:8080 -> enrolment-service:5001 -> database-service:5002 -> SQLite
                                      |
                                      +-> Ollama on the host
```

- `frontend-service`: Nginx, HTML, CSS, tabs, forms, and browser interaction.
- `enrolment-service`: Flask routes, validation, formatting, prompt loading, database API integration, and Ollama calls.
- `database-service`: SQLite initialization, persistence, and JSON data APIs.
- `agentic_loop`: modular DB, endpoint, architecture, and DevOps evidence reviews.
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

Menu options are DB, Endpoints, Architecture, DevOps, Run All, and Exit.

## Lab 05 CI

The manual [Lab 5 workflow](.github/workflows/lab5-ci.yml) builds all three
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
.venv/bin/python -m unittest discover -s tests -v
```

Stop the application:

```bash
docker compose down
```

See [evidence_log.md](evidence_log.md) for endpoint results, NFR timing, prompt-improvement comparisons, and reflections.
