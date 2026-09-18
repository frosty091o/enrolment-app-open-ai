# Lab 03 Evidence Log

Run date: 28 August 2026

## Validation Results

| Check | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- |
| Prompt folder created | Yes | `prompts/` contains all five required prompt files | Pass |
| Prompt files created | Yes | Implementation, context QA, and review prompts are present | Pass |
| `qwen2.5:0.5b` installed | Yes | Listed by `ollama list` | Pass |
| `llama3.1:8b` installed | Yes | Listed by `ollama list` | Pass |
| Context form added to frontend | Yes | HTMX form posts to `/ask-with-context` | Pass |
| Task 1: `/ask-with-context` works | Yes | HTTP 200 with a context-constrained answer | Pass |
| NFR: by-subject <= 500 ms (19/20 requests) | Pass | 20/20 passed; average 0.001562 s, maximum 0.001989 s | Pass |
| Task 2: agentic loop live endpoint checks | All HTTP 200 | `/students`, student by ID, subject search, and `/ask` returned HTTP 200 | Pass |
| Task 2: implementation agent output | Returned | `No evidence-backed improvement identified.` | Pass |
| Task 2: review agent output | Returned | Exact three-line no-risk response returned | Pass |
| Task 3: prompt fix applied and rerun | Recorded | Review-task decision rules added and loop rerun | Pass |
| Task 3: `/ask` endpoint responds after fix | HTTP 200, no timeout | HTTP 200 in 0.339678 s | Pass |
| Task 3: human decision recorded | Recorded | Accept | Pass |

## Improvement Cycle

Improvement applied: Updated `prompts/review_task_prompt.txt` so the reviewer stays within the subject-code-search scope, treats repeated subject codes as valid, and uses the exact no-risk response when both the evidence and implementation recommendation identify no issue.

Before: The review agent reacted to an unrelated `/ask` timeout and recommended increasing its timeout even though the implementation task was reviewing subject-code search. The human decision was Reject.

After: Database validation passed for all 10 students, the ASD101 search correctly returned both matching students, all live endpoint checks returned HTTP 200, and the reviewer returned:

```text
Risk: No evidence-backed risk identified.
Correction: No correction required.
Retest: Repeat validation after future changes.
```

Evidence: The final agentic-loop run completed every PLAN -> ACT -> OBSERVE -> IMPLEMENTATION AGENT -> REVIEW AGENT -> HUMAN REVIEW -> ADAPT stage. The final `/ask` check returned HTTP 200 and the subject-search NFR passed 20/20 requests.

Human decision: Accept.

## Reflection

1. The review-task decision gate improved output quality most because it stopped the reviewer from turning valid duplicate subject codes or unrelated endpoint timing into invented subject-search defects.
2. The baseline reviewer identified an `/ask` timeout, but human review rejected it because it was outside the subject-code-search scope.
3. The live endpoint evidence had the greatest impact because it showed both the transient timeout before the fix and HTTP 200 responses after the rerun.
4. The next automation should validate agent output against its required scope and exact output format before human review.

---

# Lab 04 Evidence Log

Run date: 28 August 2026

## Environment and Deployment

| Check | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- |
| `.env` updated | `FLASK_BASE_URL=http://localhost:5001` | Added with both Ollama model variables | Pass |
| Requests dependency | `requests` listed | Present in root and enrolment-service requirements | Pass |
| Docker and Compose | Available | Docker 29.7.2 and Compose 5.4.0 | Pass |
| Ollama models | Both models installed | `qwen2.5:0.5b` and `llama3.1:8b` listed | Pass |
| Microservices build | `docker compose up --build` succeeds | All three images built successfully | Pass |
| Containers running | Three services | frontend, enrolment, and database containers running | Pass |
| Frontend accessible | HTTP 200 on port 8080 | `GET http://localhost:8080` returned 200 | Pass |
| Flask accessible | HTTP 200 on port 5001 | `GET http://localhost:5001/` returned 200 | Pass |
| Database accessible | HTTP 200 on port 5002 | Health and student APIs returned 200 | Pass |
| Container-to-Ollama access | HTTP 200 | Enrolment container reached `/api/tags` on the host | Pass |
| Database initialized | 10 records | 10 total records and 2 valid ASD101 records | Pass |

## Application and API Validation

| Check | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- |
| Normal UI tab | Loads | `/tabs/normal.html` returned 200 | Pass |
| AI Mode tab | Loads | `/tabs/ai-mode.html` returned 200 | Pass |
| Student list | HTTP 200 | `/students` returned 200 | Pass |
| Student by ID | HTTP 200 | ID 1 returned 200 | Pass |
| Invalid student ID | HTTP 400 | `student_id=abc` returned 400 | Pass |
| Missing student | HTTP 404 | ID 9999 returned 404 | Pass |
| Subject search | HTTP 200 | ASD101 returned both matching students | Pass |
| Missing subject | HTTP 404 | ABC999 returned 404 | Pass |
| `/ask` | Valid AI response | HTTP 200 | Pass |
| `/ask-with-context` | Grounded response | HTTP 200; only documented fields and endpoints returned | Pass |
| `/pattern-selection` | Valid AI response | HTTP 200 | Pass |
| `/architecture-review` | Evidence-based architecture response | HTTP 200 | Pass |
| `/adr-review` | ADR feedback returned | HTTP 200; no evidence-backed weakness identified | Pass |
| Subject-search NFR | At least 19/20 <= 0.500 s | 20/20; average 0.003921 s, maximum 0.005452 s | Pass |

## Modular Agentic Loop

| Check | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- |
| Loop starts | Menu displayed | `AGENTIC LOOP (MODULAR)` displayed | Pass |
| Menu options | DB, Endpoints, Architecture, Run All, Exit | Options 1, 2, 3, 4, and 0 displayed | Pass |
| Prompt map | Service and Lab 04 roots | Correct absolute prompt-family paths displayed | Pass |
| DB evidence | 10 valid rows | 10 valid rows and ASD101 count 2 collected | Pass |
| Endpoint evidence | Live status and timing | All nine discovered routes returned HTTP 200 with timings | Pass |
| Architecture evidence | Three boundaries and Compose topology | All required files, services, network, and volume confirmed | Pass |
| Stage banners | START through DONE | START, OBSERVE, PROMPTS, LLM, and DONE shown for every mode | Pass |
| Service prompts | Loaded from `prompts/service` | DB and Endpoints modes loaded the implementation set | Pass |
| Lab 04 prompts | Loaded from `prompts/lab4` | Architecture implementation and review prompts loaded | Pass |
| Placeholder injection | No unresolved placeholders | Verified by automated test | Pass |
| Final DB output | Evidence-based | `No evidence-backed improvement identified.` | Pass |
| Final Endpoints output | Evidence-based | `No evidence-backed improvement identified.` | Pass |
| Final Architecture output | Evidence-based boundaries | Correct ownership and frontend -> enrolment -> database direction | Pass |
| Final architecture review | Review feedback captured | No evidence-backed correction required | Pass |

## Improvement Cycles

### Database review

- Review Target: DB
- Prompt Changed: `prompts/service/implementation/context_prompt.txt`
- Before: The implementation model recommended making `subject_code` unique even though the evidence showed two valid ASD101 enrolments.
- After: `No evidence-backed improvement identified.`
- Evidence: The collector confirmed 10 valid rows, two ASD101 rows, and no failed database check.
- Decision: Reject the original recommendation; Accept the corrected output.

### Endpoint review

- Review Target: Endpoints
- Prompt Changed: `prompts/service/implementation/task_prompt.txt`
- Before: The model proposed subject-code uniqueness, HTTP 409 handling, and changing HTML responses to JSON despite every live route returning 200.
- After: `No evidence-backed improvement identified.`
- Evidence: All nine discovered enrolment-service routes returned HTTP 200 without timeout, connection failure, or error.
- Decision: Reject the unsupported recommendation; Accept the corrected output.

### Architecture review

- Review Target: Architecture
- Prompt Changed: `prompts/lab4/implementation/architecture_task_prompt.txt`
- Before: The model invented organizational ownership and incorrectly suggested reverse database dependencies.
- After: `Boundaries are clear: frontend-service owns presentation, enrolment-service owns application and AI integration, and database-service owns persistence. The verified dependency direction is frontend-service to enrolment-service to database-service; no missing responsibility is evidenced.`
- Evidence: The architecture collector verified all service files and the three-service Compose topology; the review model reported no evidence-backed correction.
- Decision: Reject the speculative output; Accept the grounded output.

## Architecture Artifacts

- ADR: `architecture/ADR-001-three-service-architecture.md`
- Service boundary record: `architecture/service-boundaries.md`
- ADR decision: Use frontend-service, enrolment-service, and database-service with a private Compose network and persistent database volume.
- ADR feedback: The live ADR-review endpoint returned `No evidence-backed ADR weakness identified.`
- Adaptation: Architecture prompts now forbid invented organizational ownership and reverse dependencies.

## Automated Verification

- Seven `unittest` checks pass for prompt resolution, placeholder replacement, database evidence, architecture evidence, endpoint decision gating, HTML escaping, and context-answer grounding.
- Python compilation passes for all root, service, agent-loop, and test modules.
- `docker compose config --quiet` passes.
- `git diff --check` passes.

## Lab 04 Reflection

1. Microservices suit Normal UI and AI Mode separation because the static interface remains independently deployable while both flows share one validated application API; model concerns stay out of the frontend and database service.
2. Separating database ownership improved maintainability most because SQL, schema initialization, and persistence now have one owner while the enrolment service consumes a stable JSON boundary.
3. The agentic loop validated the decision using 10 real database rows, live HTTP statuses and timings, required service files, and the actual Compose topology rather than assumptions.
4. The most important production-readiness change is replacing the Flask development servers with a production WSGI deployment plus health checks; authentication, secrets, observability, and database migration management follow from that baseline.

---

# Lab 05 Evidence Log

Validation date: 18 September 2026. [GitHub Actions run 35307150362](https://github.com/frosty091o/enrolment-app-open-ai/actions/runs/35307150362) passed on `main` at commit `a667a005de5ec03f4a3b5923ad555da5e33e2682`.

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Workflow file | Manual build, smoke, evidence jobs | `.github/workflows/lab5-ci.yml` ran via `workflow_dispatch` | Pass |
| Container build | Three images build | `docker compose up --build -d` built all three images | Local pass |
| Service smoke checks | HTTP 200 on 8080, 5001, 5002 | All three returned HTTP 200 locally | Local pass |
| Workflow build job | Three images build | `build-images` succeeded in 15 seconds | Pass |
| Workflow smoke job | All three services return HTTP 200; teardown runs | `smoke-check` succeeded in 46 seconds; `Smoke checks` and `Stop services` steps both succeeded | Pass |
| Evidence job | Generate reports and upload artifact | `evidence-pack` succeeded in 4 seconds | Pass |
| Artifact generation | Three reports with real run metadata | Downloaded `report.json`, `report.md`, `run-view.md`; run ID, commit, branch and URL agree | Pass |
| Artifact upload | `lab5-report` available from GitHub Actions | Artifact downloaded; ZIP SHA-256 matches GitHub's `bd8a888d00bbaf8b115a6d3f5acd81b748e510079deea2b7b28ce3f72f41ed6a` | Pass |
| DevOps review mode | Option 4, collector, implementation and review prompts | Real run and artifact verified; implementation and review model outputs captured | Pass |
| Regression checks | Earlier tests still pass | Nine tests passed, including two Lab 5 evidence tests | Pass |

## Prompt improvement cycle and final decision

- Review target: DevOps.
- Prompts changed: `prompts/lab5/implementation/devops_pipeline_review_prompt.txt` and `prompts/lab5/review/devops_evidence_review_prompt.txt`.
- Before: The implementation model recommended automating build, smoke and evidence stages that were already automated; the review model incorrectly approved it.
- After implementation: `Improvement: Cache Docker layers. Reason: Smoke-check rebuilds images on a separate runner. Impact: Reduce repeated work and shorten CI time.`
- After review: `Approved: Caching targets repeated builds. Evidence: Smoke-check rebuilds images on a separate runner. Retest: Compare CI run times.`
- Evidence: The workflow runs `docker compose build` in `build-images`, then `docker compose up --build -d` in a separate `smoke-check` job. GitHub confirms all three jobs succeeded and the artifact is available.
- Human decision: **Accept** the corrected, evidence-backed recommendation as a future CI improvement. The current workflow passes Lab 5; measure before and after timings if caching is implemented.

**Final CI decision: Pass.** Build, smoke validation, evidence generation and artifact upload succeeded in the real GitHub Actions run. The downloaded report files identify that run.

## Reflection

1. The GitHub smoke-check job provided the strongest evidence because it validated all three services in the runner environment.
2. The DevOps collector checks workflow structure, report consistency, live job conclusions and artifact availability; it refuses missing or placeholder run evidence.
3. Repeated image builds are the next workflow improvement to evaluate using measured GitHub timings.
4. This CI configuration passed its release readiness gate because build, smoke, evidence generation and artifact upload all succeeded. Deployment is outside Lab 5.

---

# Lab 07 Evidence Log

Run date: 18 September 2026. The MCP server, browser tab, Flask routes, collector, pipeline, prompts, and four evidence reports were added to the Lab 04–05 project.

| Check | Expected | Actual | Result |
| --- | --- | --- | --- |
| MCP server | Four read-only tools | All four listed and invoked through MCP 2.2.0 | Pass |
| Student tools | Existing data | 10 students; two ASD101 rows | Pass |
| Project files | Names within project | 25 entries; `.env` hidden; traversal rejected | Pass |
| CI report | Lab 5 JSON metadata | Run `35310145492` on `main` read; all three jobs passed | Pass |
| Web UI | MCP tab and ON/OFF switch | OFF disabled buttons; ON displayed all four results in Chrome | Pass |
| Flask routes | Browser-to-MCP calls | Four valid requests returned HTTP 200; OFF returned 403 | Pass |
| Agentic loop | Mode 5 MCP and Run All | Mode 5 completed OBSERVE, IMPLEMENTATION, and REVIEW | Pass |
| Tests | Existing and new checks | 12 tests passed | Pass |

The initial review model suggested that `ci_report` should decide release approval. Human review rejected this because the tool boundary is to read CI evidence only. The review prompt was corrected and the final model response reported no demonstrated defect. The main implementation risk is remote access without authentication or audit logging; the Compose host port is bound to loopback for this local lab. See `reports/run-report.md`, `reports/boundary-analysis.md`, `reports/tool-review.md`, and `reports/integration-report.md` for details.

---
