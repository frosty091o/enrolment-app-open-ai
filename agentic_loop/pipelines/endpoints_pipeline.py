import re


def build_user_prompt(task_prompt: str, context_prompt: str, evidence: str) -> str:
    task = task_prompt.replace("{{REVIEW_TARGET}}", "Endpoints")
    task = task.replace("{{VALIDATION_EVIDENCE}}", evidence)
    statuses = re.findall(r"returned (\d{3})", evidence)
    all_passed = bool(statuses) and all(status == "200" for status in statuses) and not any(
        marker in evidence for marker in ("TIMEOUT", "CONNECTION REFUSED", "ERROR:")
    )
    if all_passed:
        return (
            "Review Target: Endpoints\n\n"
            f"Observed Evidence:\n{evidence}\n\n"
            "Every observed endpoint returned HTTP 200 with no timeout, connection "
            "failure, or error. Output exactly this sentence and nothing else:\n"
            "No evidence-backed improvement identified."
        )

    decision_gate = (
        "Identify one issue supported directly by a failed endpoint observation."
    )
    return (
        f"{decision_gate}\n\n{task}\n\nApplication Context:\n{context_prompt}"
        f"\n\nFINAL DECISION GATE:\n{decision_gate}"
    ).strip()
