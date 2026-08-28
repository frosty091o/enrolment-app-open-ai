from flask import Blueprint, request

from services.llm_client import OLLAMA_MODEL, call_architecture_agent, create_chat_completion
from services.prompt_loader import load_prompt


ai_mode_bp = Blueprint("ai_mode", __name__)

CONTEXT_FALLBACK = (
    "The Student Enrolment App provides read-only access to student_id, "
    "student_name, and subject_code through GET /students, /students/{student_id}, "
    "/students/by-id, and /students/by-subject. AI questions use POST /ask and "
    "/ask-with-context. subject_code is not unique; multiple students may enrol "
    "in the same subject."
)


def _context_answer_is_grounded(answer):
    normalized = answer.lower()
    forbidden_claims = (
        "post /students",
        "put /students",
        "patch /students",
        "delete /students",
        "create a new student",
        "update a student",
        "delete a student",
    )
    return bool(answer.strip()) and not any(claim in normalized for claim in forbidden_claims)


@ai_mode_bp.post("/ask")
def ask_local_agent():
    question = request.form.get("question", "").strip()
    if not question:
        return "<p>Question is required.</p>", 400

    try:
        answer = create_chat_completion(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a concise software engineering assistant. "
                        "Answer in one short paragraph unless asked otherwise."
                    ),
                },
                {"role": "user", "content": question},
            ],
            max_tokens=200,
            temperature=0.2,
            model=OLLAMA_MODEL,
        )
        return f"<p>{answer}</p>", 200
    except Exception as exc:
        return (
            "<p>Local AI agent request failed. "
            "Check that Ollama is running and that qwen2.5:0.5b is installed.</p>"
            f"<pre>{exc}</pre>",
            503,
        )


@ai_mode_bp.post("/ask-with-context")
def ask_with_context():
    question = request.form.get("question", "").strip()
    if not question:
        return "<p>Question is required.</p>", 400

    try:
        system_prompt = load_prompt("service/implementation/system_prompt.txt")
        context_prompt = load_prompt("service/implementation/context_prompt.txt")
        final_prompt = (
            f"{context_prompt}\n\n"
            "Task: Answer the user question using only the application context above. "
            "Do not propose changes. If the answer is absent, say information is unavailable. "
            "Use no more than 60 words.\n\n"
            f"User Question:\n{question}"
        )
        answer = create_chat_completion(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ],
            max_tokens=300,
            temperature=0.2,
            model=OLLAMA_MODEL,
        )
        if not _context_answer_is_grounded(answer):
            answer = CONTEXT_FALLBACK
        return f"<p>{answer}</p>", 200
    except Exception as exc:
        return "<p>Context-aware request failed.</p>" f"<pre>{exc}</pre>", 503


def _architecture_request():
    return request.form.get("architecture_request", "").strip()


@ai_mode_bp.post("/pattern-selection")
def pattern_selection():
    architecture_request = _architecture_request()
    if not architecture_request:
        return "<p>Architecture request is required.</p>", 400
    try:
        answer = call_architecture_agent(
            "architecture_system_prompt.txt",
            "pattern_selection_prompt.txt",
            architecture_request,
        )
        return f"<pre>{answer}</pre>", 200
    except Exception as exc:
        return "<p>Pattern selection request failed.</p>" f"<pre>{exc}</pre>", 503


@ai_mode_bp.post("/architecture-review")
def architecture_review():
    architecture_request = _architecture_request()
    if not architecture_request:
        return "<p>Architecture request is required.</p>", 400
    try:
        evidence = (
            "Verified evidence: frontend-service owns HTML, CSS, tabs, and browser "
            "interaction; enrolment-service owns public routes, validation, HTML "
            "formatting, prompt loading, database API calls, and Ollama integration; "
            "database-service owns SQLite persistence, seeding, and JSON data APIs. "
            "The dependency direction is frontend-service to enrolment-service to "
            "database-service. Docker Compose defines all three services, one private "
            "network, and a persistent database volume."
        )
        answer = call_architecture_agent(
            "architecture_system_prompt.txt",
            "architecture_task_prompt.txt",
            f"{evidence}\n\nReview request: {architecture_request}",
        )
        return f"<pre>{answer}</pre>", 200
    except Exception as exc:
        return "<p>Architecture review request failed.</p>" f"<pre>{exc}</pre>", 503


@ai_mode_bp.post("/adr-review")
def adr_review():
    architecture_request = _architecture_request()
    if not architecture_request:
        return "<p>ADR text is required.</p>", 400
    try:
        answer = call_architecture_agent(
            "architecture_system_prompt.txt",
            "adr_review_prompt.txt",
            architecture_request,
        )
        return f"<pre>{answer}</pre>", 200
    except Exception as exc:
        return "<p>ADR review request failed.</p>" f"<pre>{exc}</pre>", 503
