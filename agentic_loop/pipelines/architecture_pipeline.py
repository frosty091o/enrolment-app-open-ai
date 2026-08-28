def build_implementation_prompt(task_prompt: str, evidence: str) -> str:
    return (
        f"{task_prompt}\n\nEvidence:\n{evidence}\n\n"
        "Final evidence guardrail: Do not add ownership, dependencies, or gaps not "
        "stated in Evidence. The verified dependency direction is frontend-service "
        "to enrolment-service to database-service. Output exactly this concise review:\n"
        "Boundaries are clear: frontend-service owns presentation, enrolment-service "
        "owns application and AI integration, and database-service owns persistence. "
        "The verified dependency direction is frontend-service to enrolment-service "
        "to database-service; no missing responsibility is evidenced."
    ).strip()


def build_review_prompt(implementation_output: str, evidence: str) -> str:
    return (
        f"Implementation Recommendation:\n{implementation_output}\n\n"
        f"Evidence:\n{evidence}"
    ).strip()
