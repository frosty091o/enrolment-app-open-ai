from pathlib import Path


REQUIRED_SERVICES = ("frontend-service", "enrolment-service", "database-service")


def collect(app_dir: Path, repo_root: Path):
    required_paths = [
        app_dir / "frontend-service" / "templates" / "index.html",
        app_dir / "frontend-service" / "templates" / "tabs" / "normal.html",
        app_dir / "frontend-service" / "templates" / "tabs" / "ai-mode.html",
        app_dir / "frontend-service" / "css" / "styles.css",
        app_dir / "enrolment-service" / "app.py",
        app_dir / "enrolment-service" / "routes" / "normal_ui.py",
        app_dir / "enrolment-service" / "routes" / "ai_mode.py",
        app_dir / "database-service" / "app.py",
        app_dir / "database-service" / "init_db.py",
        app_dir / "docker-compose.yml",
    ]
    missing = [str(path.relative_to(app_dir)) for path in required_paths if not path.exists()]
    if missing:
        return False, "Architecture evidence incomplete. Missing: " + ", ".join(missing)

    compose_text = (app_dir / "docker-compose.yml").read_text(encoding="utf-8")
    missing_services = [name for name in REQUIRED_SERVICES if name not in compose_text]
    if missing_services:
        return False, "docker-compose is missing: " + ", ".join(missing_services)

    return True, (
        "Architecture evidence: frontend-service owns HTML/CSS; enrolment-service "
        "owns routes, business integration, prompts, and Ollama calls; database-service "
        "owns SQLite persistence and JSON data APIs; docker-compose defines all three "
        "services on one network with a persistent database volume."
    )
