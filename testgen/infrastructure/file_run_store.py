"""Atomic file persistence and versioned committed-suite checkpoints."""
import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from ..domain import Case
from ..persistence import RunCheckpoint
from ..suite import suite_lock

class FileRunStore:
    def write_text(self, path: Path, text: str, *, encoding="utf-8") -> int:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding=encoding, newline="\n") as stream:
                count = stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
            return count
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def read_text(self, path: Path, *, encoding="utf-8", errors="strict") -> str:
        return Path(path).read_text(encoding=encoding, errors=errors)

    def write_json(self, path: Path, value: object) -> None:
        self.write_text(path, json.dumps(value, ensure_ascii=False, indent=2))

    def read_json(self, path: Path) -> object:
        return json.loads(self.read_text(path))

    def checkpoint(self, path: Path, checkpoint: RunCheckpoint) -> None:
        payload = asdict(checkpoint)
        self._validate(payload)
        self.write_json(path, payload)

    def restore(self, path: Path) -> RunCheckpoint:
        return self._validate(self.read_json(path))

    @staticmethod
    def _validate(value) -> RunCheckpoint:
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("Unsupported checkpoint schema version")
        if value.get("stage") != "suite_locked":
            raise ValueError("Unsupported resume stage")
        if not isinstance(value.get("problem_id"), str) or not isinstance(value.get("report"), dict):
            raise ValueError("Malformed checkpoint metadata")
        rows = value.get("cases")
        if not isinstance(rows, (list, tuple)):
            raise ValueError("Malformed checkpoint cases")
        cases = []
        for row in rows:
            if not isinstance(row, dict) or any(not isinstance(row.get(k), str)
                    for k in ("id", "input", "expected", "family")):
                raise ValueError("Malformed checkpoint case")
            if not isinstance(row.get("iteration"), int) or isinstance(row["iteration"], bool):
                raise ValueError("Malformed checkpoint iteration")
            tags = row.get("coverage_tags", [])
            if not isinstance(tags, (list, tuple)) or any(not isinstance(t, str) for t in tags):
                raise ValueError("Malformed checkpoint coverage tags")
            cases.append(Case(row["id"], row["input"], row["expected"], row["family"],
                              row["iteration"], tuple(tags)))
        if len({c.id for c in cases}) != len(cases):
            raise ValueError("Duplicate checkpoint case IDs")
        report = value["report"]
        if report.get("problem_id") != value["problem_id"]:
            raise ValueError("Checkpoint problem mismatch")
        if report.get("test_suite_lock", {}).get("sha256") != suite_lock(cases)["sha256"]:
            raise ValueError("Checkpoint suite hash mismatch")
        return RunCheckpoint(1, "suite_locked", value["problem_id"], tuple(cases), report)
