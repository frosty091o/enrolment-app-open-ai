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

Local validation date: 18 September 2026. GitHub Actions evidence is pending a real run on `main`.

| Check | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Workflow file | Manual build, smoke, evidence jobs | `.github/workflows/lab5-ci.yml` defines all three in order | Local pass |
| Container build | Three images build | `docker compose up --build -d` built all three images | Local pass |
| Service smoke checks | HTTP 200 on 8080, 5001, 5002 | All three returned HTTP 200 locally | Local pass |
| Workflow teardown | Always-run `docker compose down -v` | Configured in smoke job; GitHub execution not observed | Configured |
| Artifact generation | Three reports with real run metadata | Generator and collector agree in an isolated test; no real artifact yet | Pending CI run |
| Artifact upload | `lab5-report` available from GitHub Actions | Upload step configured; not observed on GitHub | Pending CI run |
| DevOps review mode | Option 4, collector, implementation and review prompts | Option 4 starts and correctly requests downloaded reports | Local pass; live review pending |
| Regression checks | Earlier tests still pass | Nine tests passed, including two Lab 5 evidence tests | Pass |

## Improvement recommendation and decision

The smoke job rebuilds the images because GitHub Actions jobs run on separate runners.
After the first real run, review build times and consider sharing the built images or
caching layers. Expected impact: less repeated work and faster CI. **Decision:
Partially Accept** as a future improvement; its value needs timing evidence from a
real workflow run. Final CI pass/fail decision remains **pending** until all three
GitHub jobs pass and the `lab5-report` artifact is downloaded and reviewed.

## Reflection

1. The strongest local validation is the three HTTP 200 smoke checks; the GitHub run remains the required CI evidence.
2. The DevOps collector checks workflow structure and report consistency and refuses missing or placeholder run evidence.
3. Repeated image builds are the next workflow improvement to evaluate using actual GitHub timings.
4. The CI configuration is release-ready only after a real run passes build, smoke, evidence generation, and artifact upload.
