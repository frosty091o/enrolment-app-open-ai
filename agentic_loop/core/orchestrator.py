from pathlib import Path

from collectors import architecture_collector, db_collector, devops_collector, endpoints_collector
from config.review_config import ModeConfig
from core.ai_runner import AIRunner
from core.prompt_registry import PromptRegistry
from pipelines import architecture_pipeline, db_pipeline, devops_pipeline, endpoints_pipeline


COLLECTORS = {
    "db": db_collector.collect,
    "endpoints": endpoints_collector.collect,
    "architecture": architecture_collector.collect,
    "devops": devops_collector.collect,
}


def _stage(mode_label: str, step: str, message: str) -> None:
    print(f"[{mode_label}][{step}] {message}")


def run_mode(
    mode: ModeConfig,
    app_dir: Path,
    repo_root: Path,
    prompts: PromptRegistry,
    ai: AIRunner,
) -> str:
    _stage(mode.label, "START", "Starting review flow")
    _stage(mode.label, "OBSERVE", "Collecting evidence")
    ok, evidence = COLLECTORS[mode.key](app_dir, repo_root)
    if not ok:
        _stage(mode.label, "OBSERVE", "Failed")
        return f"OBSERVE FAILED: {evidence}"
    _stage(mode.label, "OBSERVE", "Complete")

    if mode.key in {"db", "endpoints"}:
        _stage(mode.label, "PROMPTS", f"Loading prompt family: {mode.prompt_family}")
        system_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[0])
        task_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[1])
        context_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[2])
        _stage(mode.label, "PROMPTS", "Loaded implementation prompt set")

        pipeline = db_pipeline if mode.key == "db" else endpoints_pipeline
        user_prompt = pipeline.build_user_prompt(task_prompt, context_prompt, evidence)
        _stage(mode.label, "LLM", "Running implementation model")
        output, error = ai.call(system_prompt, user_prompt)
        if error:
            _stage(mode.label, "LLM", "Failed")
            return f"MODEL FAILED: {error}"
        _stage(mode.label, "LLM", "Complete")
        _stage(mode.label, "DONE", "Review complete")
        return f"OBSERVE: {evidence}\n\nREVIEW: {output}"

    if mode.key == "architecture":
        _stage(mode.label, "PROMPTS", f"Loading prompt family: {mode.prompt_family}")
        system_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[0])
        task_prompt = prompts.read(mode.prompt_family, mode.implementation_prompts[1])
        implementation_prompt = architecture_pipeline.build_implementation_prompt(
            task_prompt, evidence
        )
        _stage(mode.label, "PROMPTS", "Loaded architecture implementation prompts")
        _stage(mode.label, "LLM", "Running architecture model")
        implementation_output, error = ai.call(system_prompt, implementation_prompt)
        if error:
            _stage(mode.label, "LLM", "Failed")
            return f"MODEL FAILED: {error}"
        _stage(mode.label, "LLM", "Architecture model complete")

        review_system_prompt = prompts.read(mode.prompt_family, mode.review_prompts[0])
        review_prompt = architecture_pipeline.build_review_prompt(
            implementation_output, evidence
        )
        _stage(mode.label, "PROMPTS", "Loaded architecture review prompt")
        _stage(mode.label, "LLM", "Running review model")
        review_output, review_error = ai.call(
            review_system_prompt, review_prompt, review=True
        )
        if review_error:
            review_output = review_error
            _stage(mode.label, "LLM", "Review model failed")
        else:
            _stage(mode.label, "LLM", "Review model complete")
        _stage(mode.label, "DONE", "Review complete")
        return (
            f"OBSERVE: {evidence}\n\n"
            f"ARCHITECTURE: {implementation_output}\n"
            f"REVIEW: {review_output}"
        )

    if mode.key == "devops":
        _stage(mode.label, "PROMPTS", "Loading Lab 5 prompts")
        task_prompt = prompts.read_stage(mode.prompt_family, "implementation")
        review_prompt = prompts.read_stage(mode.prompt_family, "review")
        implementation_input = devops_pipeline.build_implementation_prompt(
            task_prompt, evidence
        )
        _stage(mode.label, "LLM", "Running DevOps implementation review")
        implementation_output, error = ai.call(
            "Use only supplied DevOps evidence; reply in at most 30 words.",
            implementation_input,
            word_limit=30,
        )
        if error:
            _stage(mode.label, "LLM", "Failed")
            return f"MODEL FAILED: {error}"

        review_input = devops_pipeline.build_review_prompt(
            implementation_output, evidence
        )
        _stage(mode.label, "LLM", "Running DevOps evidence review")
        review_output, error = ai.call(
            review_prompt, review_input, review=True, word_limit=30
        )
        if error:
            _stage(mode.label, "LLM", "Review failed")
            return f"OBSERVE: {evidence}\n\nDEVOPS: {implementation_output}\nREVIEW FAILED: {error}"
        _stage(mode.label, "DONE", "Review complete")
        return (
            f"OBSERVE: {evidence}\n\n"
            f"DEVOPS: {implementation_output}\nREVIEW: {review_output}"
        )

    return "Unknown mode."
