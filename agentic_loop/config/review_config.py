from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ModeConfig:
    key: str
    label: str
    prompt_family: str
    implementation_prompts: Tuple[str, ...]
    review_prompts: Tuple[str, ...] = ()


def build_mode_config() -> Dict[str, ModeConfig]:
    service_prompts = (
        "implementation/system_prompt.txt",
        "implementation/task_prompt.txt",
        "implementation/context_prompt.txt",
    )
    return {
        "db": ModeConfig("db", "DB", "service", service_prompts),
        "endpoints": ModeConfig("endpoints", "Endpoints", "service", service_prompts),
        "architecture": ModeConfig(
            "architecture",
            "Architecture",
            "lab4",
            (
                "implementation/architecture_system_prompt.txt",
                "implementation/architecture_task_prompt.txt",
            ),
            ("review/agent_review_prompt.txt",),
        ),
        "devops": ModeConfig(
            "devops",
            "DevOps",
            "lab5",
            ("implementation/devops_pipeline_review_prompt.txt",),
            ("review/devops_evidence_review_prompt.txt",),
        ),
    }
