# ADR-001: Three-Service Architecture

- Status: Accepted
- Date: 28 August 2026

## Context

Lab 03 deployed the HTMX interface, Flask routes, Ollama integration, and SQLite access as one application. Lab 04 requires independently deployable presentation and backend components, an independently managed database lifecycle, and clearer Normal UI and AI Mode ownership.

## Decision

Use a containerized three-service architecture:

- `frontend-service` owns static HTML, CSS, tab composition, and browser interaction.
- `enrolment-service` owns HTTP-facing application routes, input validation, HTML response formatting, database-service integration, prompt loading, and Ollama integration.
- `database-service` exclusively owns SQLite persistence, initialization, and JSON data APIs.

Docker Compose supplies one private application network and a named volume for database persistence. The browser reaches ports 8080 and 5001; internal backend-to-database communication uses the Docker service name on port 5002.

## Alternatives

- Retain the Lab 03 monolith: simplest deployment, but it does not meet the required independent service lifecycles.
- Use only layered modules inside one deployment: improves code organization, but not deployment independence.
- Use PostgreSQL immediately: stronger multi-client database capabilities, but not supported by current scale evidence and adds unnecessary operational scope.

## Trade-offs

The design improves ownership, modularity, and independent deployment at the cost of Docker orchestration, HTTP failure modes, CORS configuration, additional logs, and more complex testing.

## Consequences

Frontend changes can deploy without rebuilding database code. Persistence survives container replacement through a named volume. Database access is centralized behind JSON endpoints. Production deployment will still require authentication, health checks, secret management, observability, and a production WSGI server.
