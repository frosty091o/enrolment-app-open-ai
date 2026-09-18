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

    def read_stage(self, family: str, stage: str) -> str:
        """Load every text prompt in one implementation or review stage."""
        if stage not in {"implementation", "review"}:
            raise ValueError("Prompt stage must be implementation or review")
        stage_dir = (self.root / family / stage).resolve()
        if self.root not in stage_dir.parents or not stage_dir.is_dir():
            raise FileNotFoundError(f"Missing prompt stage: {family}/{stage}")
        files = sorted(stage_dir.glob("*.txt"))
        if not files:
            raise FileNotFoundError(f"No prompts in: {family}/{stage}")
        return "\n\n".join(self.read(family, f"{stage}/{path.name}") for path in files)
