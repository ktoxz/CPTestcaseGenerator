"""Declarative language/runtime selection shared by generation and judging."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .domain import Solution


DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "config" / "runtimes.json"


@dataclass(frozen=True)
class RuntimeSpec:
    id: str
    language: str
    dialects: tuple[str, ...]
    extension: str
    source_file: str
    image: str
    compile: str
    execute: str
    llm: bool = False


class RuntimeCatalog:
    def __init__(self, path: Path = DEFAULT_CATALOG):
        self.path = path
        data = json.loads(path.read_text(encoding="utf-8"))
        self.images: dict[str, dict] = data["images"]
        self.prompt_notes: tuple[str, ...] = tuple(data.get("prompt_notes", []))
        self.runtimes = [RuntimeSpec(**{**row, "dialects": tuple(row["dialects"])})
                         for row in data["runtimes"]]
        self._by_language_dialect: dict[tuple[str, str], RuntimeSpec] = {}
        self.extensions: dict[str, str] = {}
        for runtime in self.runtimes:
            if runtime.image not in self.images:
                raise ValueError(f"Unknown image {runtime.image} for {runtime.id}")
            if runtime.language in self.extensions and self.extensions[runtime.language] != runtime.extension:
                raise ValueError(f"Inconsistent extension for {runtime.language}")
            self.extensions[runtime.language] = runtime.extension
            for dialect in runtime.dialects:
                key = (runtime.language, dialect)
                if key in self._by_language_dialect:
                    raise ValueError(f"Duplicate runtime for {key}")
                self._by_language_dialect[key] = runtime

    def resolve(self, solution: Solution) -> RuntimeSpec:
        key = (solution.language, solution.dialect)
        if key not in self._by_language_dialect:
            raise ValueError(f"No runtime for language/dialect {key}")
        return self._by_language_dialect[key]

    def llm_languages(self) -> list[str]:
        return list(dict.fromkeys(runtime.language for runtime in self.runtimes if runtime.llm))

    def images_to_build(self, include_oracle: bool) -> list[dict]:
        return [image for image in self.images.values()
                if include_oracle or not image.get("oracle_only", False)]
