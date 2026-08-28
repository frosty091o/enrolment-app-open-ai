from pathlib import Path


class PromptRegistry:
    def __init__(self, app_dir: Path):
        self.app_dir = app_dir.resolve()
        self.root = (self.app_dir / "prompts").resolve()

    def resolve(self, family: str, relative_file: str) -> Path:
        candidate = (self.root / family / relative_file).resolve()
        if self.root not in candidate.parents:
            raise ValueError("Prompt path must remain inside the prompt directory")
        if not candidate.is_file():
            raise FileNotFoundError(
                f"Missing prompt file: {candidate.relative_to(self.app_dir)}"
            )
        return candidate

    def read(self, family: str, relative_file: str) -> str:
        content = self.resolve(family, relative_file).read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Prompt file is empty: {family}/{relative_file}")
        return content

    def family_path(self, family: str) -> Path:
        return self.root / family
