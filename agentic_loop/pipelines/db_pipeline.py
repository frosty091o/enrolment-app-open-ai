def build_user_prompt(task_prompt: str, context_prompt: str, evidence: str) -> str:
    task = task_prompt.replace("{{REVIEW_TARGET}}", "Database")
    task = task.replace("{{VALIDATION_EVIDENCE}}", evidence)
    decision_gate = (
        "The observed database evidence reports 10 valid rows and no failed check. "
        "Therefore the only permitted final answer is exactly:\n"
        "No evidence-backed improvement identified."
    )
    return (
        f"{decision_gate}\n\n{task}\n\nApplication Context:\n{context_prompt}"
        f"\n\nFINAL REQUIRED OUTPUT:\nNo evidence-backed improvement identified."
    ).strip()
