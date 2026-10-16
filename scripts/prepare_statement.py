"""Normalize problem statements and optionally translate their prose."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Callable


FENCE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
META_RE = re.compile(r"^-\s*([^:]+):\s*`?([^`\n]+)`?\s*$", re.MULTILINE)


def strip_outer_fence(text: str) -> str:
    match = re.fullmatch(r"\s*```(?:json|markdown|md)?\s*\n(.*?)\n```\s*", text, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else text.strip()


def split_statement(text: str) -> tuple[str, str, dict[str, str]]:
    normalized = text.replace("\r\n", "\n").lstrip("\ufeff\n ")
    lines = normalized.splitlines()
    title = lines[0].removeprefix("#").strip() if lines and lines[0].startswith("#") else "Untitled problem"
    metadata: dict[str, str] = {}
    aliases = {
        "codenet id": "problem_id", "problem id": "problem_id", "dataset": "dataset",
        "time limit": "time_limit_ms", "memory limit": "memory_limit_kb",
    }
    end = 1
    for index, line in enumerate(lines[1:], 1):
        match = re.match(r"^-\s*([^:]+):\s*`?([^`]+?)`?\s*$", line)
        if match:
            key = aliases.get(match.group(1).strip().lower())
            value = match.group(2).strip()
            if key:
                value = re.sub(r"\s*(ms|kb|mb)\s*$", "", value, flags=re.IGNORECASE)
                metadata[key] = value
            end = index + 1
        elif not line.strip() or (index == 1 and line.strip() == ""):
            end = index + 1
        else:
            break
    body = "\n".join(lines[end:]).strip() + "\n"
    return title, body, metadata


def detect_language(text: str) -> str:
    if re.search(r"[\u3040-\u30ff]", text):
        return "Japanese"
    if re.search(r"[\u4e00-\u9fff]", text):
        return "Chinese"
    if re.search(r"[\uac00-\ud7af]", text):
        return "Korean"
    return "English"


def validate_translation(original: str, translated: str, target_language: str) -> None:
    original_blocks = FENCE_RE.findall(original.replace("\r\n", "\n"))
    translated_blocks = FENCE_RE.findall(translated.replace("\r\n", "\n"))
    if original_blocks != translated_blocks:
        raise ValueError("Translation changed a fenced code block")
    if not translated.strip():
        raise ValueError("Translation is empty")


def _metadata_header(title: str, metadata: dict) -> str:
    problem_id = str(metadata.get("problem_id") or metadata.get("id") or "unknown")
    dataset = str(metadata.get("dataset") or "unknown")
    time_limit = metadata.get("time_limit_ms", 1000)
    memory_kb = metadata.get("memory_limit_kb")
    if memory_kb is None and metadata.get("memory_limit_mb") is not None:
        memory_kb = int(metadata["memory_limit_mb"]) * 1024
    memory_kb = memory_kb or 262144
    return (f"# {title}\n\n- CodeNet ID: `{problem_id}`\n- Dataset: `{dataset}`\n"
            f"- Time limit: `{time_limit} ms`\n- Memory limit: `{memory_kb} KB`\n\n")


def prepare_problem(
    statement_path: Path,
    output_dir: Path,
    *,
    metadata_path: Path | None = None,
    translator: Callable[[str, str, str, str], tuple[str, str]] | None = None,
    translate_mode: str = "auto",
    target_language: str = "English",
    force: bool = False,
) -> dict:
    statement_path, output_dir = Path(statement_path), Path(output_dir)
    source = statement_path.read_text(encoding="utf-8")
    title, body, embedded = split_statement(source)
    metadata = dict(embedded)
    if metadata_path and Path(metadata_path).is_file():
        metadata.update(json.loads(Path(metadata_path).read_text(encoding="utf-8")))
    metadata.setdefault("problem_id", statement_path.parent.name)
    source_language = detect_language(title + "\n" + body)
    should_translate = translate_mode == "always" or (translate_mode == "auto" and source_language != target_language)
    if should_translate:
        if translator is None:
            raise ValueError(f"A translator is required for {source_language} input")
        translated_title, translated_body = translator(title, body, source_language, target_language)
        validate_translation(body, translated_body, target_language)
        final_title, final_body = translated_title.strip(), translated_body.strip() + "\n"
    else:
        final_title, final_body = title, body
    output_dir.mkdir(parents=True, exist_ok=True)
    statement_output = output_dir / "statement.md"
    if statement_output.exists() and not force and statement_output.resolve() != statement_path.resolve():
        raise FileExistsError(f"Refusing to overwrite {statement_output}; use --force")
    prepared = _metadata_header(final_title, metadata) + final_body.lstrip()
    statement_output.write_text(prepared, encoding="utf-8")
    if should_translate:
        (output_dir / "statement.original.md").write_text(source, encoding="utf-8")
    for target in IMAGE_RE.findall(source):
        relative = target.split()[0].strip("<>")
        if re.match(r"^[a-z]+://", relative, re.IGNORECASE) or relative.startswith("data:"):
            continue
        source_image = (statement_path.parent / relative).resolve()
        try:
            source_image.relative_to(statement_path.parent.resolve())
        except ValueError:
            continue
        if source_image.is_file():
            destination = output_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source_image.resolve() != destination.resolve():
                shutil.copy2(source_image, destination)
    metadata["translation"] = {
        "performed": should_translate,
        "source_language": source_language,
        "target_language": target_language,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"problem_id": metadata["problem_id"], "translated": should_translate, "output": str(output_dir)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--statement", type=Path)
    group.add_argument("--input-root", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--translate", choices=("auto", "never", "always"), default="auto")
    parser.add_argument("--target-language", default="English")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    mode = "never" if args.translate == "never" else args.translate
    if args.statement:
        if not args.output:
            parser.error("--output is required with --statement")
        result = prepare_problem(args.statement, args.output, metadata_path=args.metadata,
                                 translate_mode=mode, target_language=args.target_language,
                                 force=args.force)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    if not args.output_root:
        parser.error("--output-root is required with --input-root")
    results = []
    for statement in sorted(args.input_root.glob("*/statement.md")):
        metadata = statement.with_name("metadata.json")
        results.append(prepare_problem(statement, args.output_root / statement.parent.name,
                                       metadata_path=metadata if metadata.exists() else None,
                                       translate_mode=mode, target_language=args.target_language,
                                       force=args.force))
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
