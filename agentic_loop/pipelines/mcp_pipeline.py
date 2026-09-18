"""Build concise, evidence-grounded Lab 7 implementation and review prompts."""

import json


def compact_evidence(evidence: str) -> str:
    results = json.loads(evidence.split(": ", 1)[1])
    students = results["students_by_subject"]
    report = results["ci_report"]
    return (
        "Four MCP tools were listed and executed successfully. "
        f"student_count: {results['student_count']['student_count']}. "
        f"students_by_subject(ASD101): {len(students)} records, "
        f"{', '.join(row['student_name'] for row in students)}. "
        f"project_files(.): {len(results['project_files'])} entries, including "
        f"{', '.join(results['project_files'][:5])}. "
        f"ci_report: workflow {report['workflow_name']}, run {report['run_id']}, "
        f"branch {report['branch']}, commit {report['commit_sha']}. "
        "The CI tool reports metadata, not release approval."
    )


def build_implementation_prompt(task_prompt: str, evidence: str) -> str:
    return f"{task_prompt}\n\nACTUAL_MCP_TOOL_RESULTS:\n{compact_evidence(evidence)}\n\nUse only these results."


def build_review_prompt(implementation_output: str, evidence: str) -> str:
    return (
        f"IMPLEMENTATION_RECOMMENDATION:\n{implementation_output}\n\n"
        f"ACTUAL_MCP_TOOL_RESULTS:\n{compact_evidence(evidence)}\n\n"
        "Check tool selection, read-only boundaries, and whether conclusions follow from results."
    )
