# Lab 04 Service Boundaries

```text
Browser
  ├─ Normal UI tab ─┐
  └─ AI Mode tab ───┴─> frontend-service :8080
                              │ HTTP
                              v
                     enrolment-service :5001 ──> Ollama on host :11434
                              │ HTTP
                              v
                      database-service :5002
                              │
                              v
                     SQLite named volume
```

| Service | Owns | Must not own |
| --- | --- | --- |
| frontend-service | HTML, CSS, tabs, forms, browser-side requests | Business rules, SQL, prompts, model calls |
| enrolment-service | Public app routes, validation, formatting, database client, prompt loading, Ollama client | SQLite files, database schema lifecycle |
| database-service | Schema, seed data, SQLite connection, JSON data APIs | HTML rendering, prompts, Ollama calls |

Normal UI and AI Mode are presentation flows within `frontend-service`. Their business and AI requests converge on `enrolment-service`, while all persistent student reads cross the `database-service` boundary.
