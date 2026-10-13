"""Artifact persistence port; serializers live behind this boundary."""
from pathlib import Path
from typing import Protocol
from dataclasses import dataclass
from .domain import Case

@dataclass(frozen=True)
class RunCheckpoint:
    schema_version: int
    stage: str
    problem_id: str
    cases: tuple[Case, ...]
    report: dict

class RunStore(Protocol):
    def write_text(self, path: Path, text: str, *, encoding: str = "utf-8") -> int: ...
    def read_text(self, path: Path, *, encoding: str = "utf-8", errors: str = "strict") -> str: ...
    def write_json(self, path: Path, value: object) -> None: ...
    def read_json(self, path: Path) -> object: ...
    def checkpoint(self, path: Path, checkpoint: RunCheckpoint) -> None: ...
    def restore(self, path: Path) -> RunCheckpoint: ...


def default_run_store() -> RunStore:
    """Compatibility composition for callers that previously supplied no storage adapter."""
    from .infrastructure.file_run_store import FileRunStore
    return FileRunStore()
