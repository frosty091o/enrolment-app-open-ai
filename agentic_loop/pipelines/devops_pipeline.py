"""Prepare evidence-grounded prompts for the Lab 5 review."""


def build_implementation_prompt(task_prompt: str, evidence: str) -> str:
    return (
        f"{task_prompt}\n\n"
        f"VALIDATION_EVIDENCE:\n{evidence}\n\n"
        "Follow the task prompt's short output format exactly."
    )


def build_review_prompt(implementation_output: str, evidence: str) -> str:
    return (
        f"IMPLEMENTATION_RECOMMENDATION:\n{implementation_output}\n\n"
        f"VALIDATION_EVIDENCE:\n{evidence}\n\n"
        "Approve only if the recommendation follows from this evidence. "
        "Otherwise state a specific risk, correction, and retest. Use at most 30 words."
    )
