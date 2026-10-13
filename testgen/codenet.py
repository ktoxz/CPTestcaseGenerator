"""Fetch bounded CodeNet oracle pools over SSH, without moving the whole dataset."""

from __future__ import annotations

import json
import hashlib
import re
import shlex
import shutil
import subprocess
import tarfile
import time
from pathlib import Path

from .domain import OracleSource, Solution
from .progress import ConsoleProgress
from .runtime import DEFAULT_CATALOG


_SOURCE_RUNTIME = {
    ".c": ("C", "C"),
    ".cc": ("C++", "C++17"),
    ".cpp": ("C++", "C++17"),
    ".cxx": ("C++", "C++17"),
    ".java": ("Java", "Java"),
    ".py": ("Python", "Python3"),
}

_ORACLE_LABELS = {
    "accepted": "Accepted",
    "ac": "Accepted",
    "wrong answer": "Wrong Answer",
    "wronganswer": "Wrong Answer",
    "wa": "Wrong Answer",
    "non-accepted": "Wrong Answer",
    "non accepted": "Wrong Answer",
}


def _normalize_oracle_label(value: object) -> str:
    raw = str(value).strip()
    normalized = _ORACLE_LABELS.get(raw.lower())
    if normalized is None:
        raise ValueError(f"Unsupported oracle label: {raw!r}")
    return normalized


def _raw_oracle_files(bundle: Path, label_dir: str) -> list[Path]:
    source_dir = bundle / "sources" / label_dir
    if not source_dir.is_dir():
        return []
    return sorted(
        (
            path for path in source_dir.iterdir()
            if path.is_file() and path.suffix.lower() in _SOURCE_RUNTIME
        ),
        key=lambda path: path.name.lower(),
    )


def _has_raw_oracle_pool(bundle: Path) -> bool:
    return bool(
        _raw_oracle_files(bundle, "Accepted")
        and _raw_oracle_files(bundle, "WrongAnswer")
    )


def find_local_oracle_bundle(
    problems_root: Path, problem_id: str
) -> Path | None:
    candidate = problems_root / problem_id / "oracle"
    return candidate if (
        (candidate / "manifest.json").is_file()
        or _has_raw_oracle_pool(candidate)
    ) else None


def _build_raw_manifest(
    output: Path, problem_id: str, per_label: int
) -> list[dict]:
    rows = []
    for label_dir, label, id_part in (
        ("Accepted", "Accepted", "ac"),
        ("WrongAnswer", "Wrong Answer", "wa"),
    ):
        sources = _raw_oracle_files(output, label_dir)
        if not sources:
            raise ValueError(
                f"Raw oracle bundle has no supported sources in "
                f"sources/{label_dir}"
            )
        for index, source in enumerate(sources[:per_label], 1):
            language, dialect = _SOURCE_RUNTIME[source.suffix.lower()]
            rows.append({
                "id": f"{problem_id}-{id_part}-{index}",
                "problem_id": problem_id,
                "label": label,
                "language": language,
                "dialect": dialect,
                "source": source.relative_to(output).as_posix(),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            })
    (output / "manifest.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return rows


def validate_codenet_request(
    problem_id: str, per_label: int, max_per_label: int
) -> None:
    if not re.fullmatch(r"p\d{5}", problem_id):
        raise ValueError(
            "CodeNet oracle requires a CodeNet problem id in the form pNNNNN; "
            f"got {problem_id!r}"
        )
    if not 1 <= per_label <= max_per_label:
        raise ValueError(
            f"CodeNet oracle limit must be between 1 and {max_per_label}; "
            f"got {per_label}"
        )


class SSHCodeNetSource(OracleSource):
    def __init__(self, exporter: Path, host: str | None = None,
                 root: str | None = None, runtime_config: Path = DEFAULT_CATALOG,
                 settings_path: Path | None = None,
                 progress: ConsoleProgress | None = None):
        settings_file = settings_path or Path(__file__).resolve().parents[1] / "config" / "oracle.json"
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        self.exporter = exporter
        self.host = host or settings["host"]
        self.root = root or settings["staging_root"]
        self.runtime_config = runtime_config
        self.pyarrow_version = settings["pyarrow_version"]
        self.max_per_label = settings["max_per_label"]
        self.progress = progress

    def _call(self, args: list[str], component: str, **details) -> str:
        started = time.monotonic()
        try:
            done = subprocess.run(
                args, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=600, check=False,
            )
        except BaseException:
            if self.progress:
                self.progress.latency(
                    component, time.monotonic() - started, status="error", **details
                )
            raise
        if self.progress:
            self.progress.latency(
                component, time.monotonic() - started,
                status="ok" if done.returncode == 0 else "error",
                returncode=done.returncode, **details,
            )
        if done.returncode:
            raise RuntimeError(f"{' '.join(args[:2])}: {done.stderr.strip() or done.stdout.strip()}")
        return done.stdout.strip()

    def fetch(self, problem_id: str, output: Path, per_label: int) -> list[Solution]:
        validate_codenet_request(problem_id, per_label, self.max_per_label)
        output.mkdir(parents=True, exist_ok=True)
        remote = self._call(
            ["ssh", "-o", "BatchMode=yes", self.host,
             "mktemp -d /tmp/testgen-export.XXXXXXXX"],
            "oracle.fetch.ssh_mktemp", host=self.host,
        )
        if not re.fullmatch(r"/tmp/testgen-export\.[A-Za-z0-9]{8}", remote):
            raise RuntimeError(f"Unexpected remote temp path: {remote!r}")
        try:
            self._call(
                ["scp", "-o", "BatchMode=yes", str(self.exporter),
                 f"{self.host}:{remote}/export.py"],
                "oracle.fetch.scp_exporter", host=self.host,
            )
            self._call(
                ["scp", "-o", "BatchMode=yes", str(self.runtime_config),
                 f"{self.host}:{remote}/runtimes.json"],
                "oracle.fetch.scp_runtime", host=self.host,
            )
            command = (f"python3 -m venv {shlex.quote(remote)}/venv "
                       f"&& {shlex.quote(remote)}/venv/bin/pip -q install pyarrow=={shlex.quote(self.pyarrow_version)} "
                       f"&& {shlex.quote(remote)}/venv/bin/python {shlex.quote(remote)}/export.py "
                       f"--root {shlex.quote(self.root)} --problem {problem_id} --limit {per_label} "
                       f"--runtime-config {shlex.quote(remote)}/runtimes.json "
                       f"--output {shlex.quote(remote)}/bundle.tar.gz")
            self._call(
                ["ssh", "-o", "BatchMode=yes", self.host, command],
                "oracle.fetch.remote_export", host=self.host,
                problem_id=problem_id, per_label=per_label,
            )
            archive = output / "bundle.tar.gz"
            self._call(
                ["scp", "-o", "BatchMode=yes",
                 f"{self.host}:{remote}/bundle.tar.gz", str(archive)],
                "oracle.fetch.scp_bundle", host=self.host,
            )
        finally:
            # The path is constrained above to a newly-created /tmp directory.
            self._call(
                ["ssh", "-o", "BatchMode=yes", self.host, f"rm -r -- {remote}"],
                "oracle.fetch.remote_cleanup", host=self.host,
            )
        extract_started = time.monotonic()
        try:
            with tarfile.open(archive, "r:gz") as package:
                members = package.getmembers()
                if any(m.name.startswith("/") or ".." in Path(m.name).parts
                       or not m.isfile() for m in members):
                    raise ValueError("Unsafe oracle archive")
                package.extractall(output, filter="data")
        except BaseException:
            if self.progress:
                self.progress.latency(
                    "oracle.fetch.extract_bundle", time.monotonic() - extract_started,
                    status="error",
                )
            raise
        if self.progress:
            self.progress.latency(
                "oracle.fetch.extract_bundle", time.monotonic() - extract_started,
                files=len(members), archive_bytes=archive.stat().st_size,
            )
        return LocalCodeNetSource(output, self.progress).fetch(
            problem_id, output, per_label
        )


class LocalCodeNetSource(OracleSource):
    """Use an already fetched bundle (e.g. WSL judge after Windows-side SSH fetch)."""

    def __init__(self, bundle: Path, progress: ConsoleProgress | None = None):
        self.bundle = bundle
        self.progress = progress

    def fetch(self, problem_id: str, output: Path, per_label: int) -> list[Solution]:
        started = time.monotonic()
        output.mkdir(parents=True, exist_ok=True)
        if self.bundle.resolve() != output.resolve():
            shutil.copytree(self.bundle, output, dirs_exist_ok=True)
        manifest = output / "manifest.json"
        rows = (
            json.loads(manifest.read_text(encoding="utf-8"))
            if manifest.is_file()
            else _build_raw_manifest(output, problem_id, per_label)
        )
        solutions = []
        for row in rows:
            if row.get("problem_id", problem_id) != problem_id:
                raise ValueError("Cached oracle bundle belongs to a different problem")
            source = (output / row["source"]).resolve()
            if not source.is_relative_to(output.resolve()):
                raise ValueError("Source path escaped oracle directory")
            if hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError(f"Source hash mismatch: {row['id']}")
            label = _normalize_oracle_label(row["label"])
            norm_label = f"CodeNet {label}"
            if sum(s.label == norm_label for s in solutions) < per_label:
                solutions.append(Solution(row["id"], norm_label, row["language"],
                                          source, dialect=row["dialect"]))
        if self.progress:
            self.progress.latency(
                "oracle.fetch.read_manifest", time.monotonic() - started,
                solutions=len(solutions), cached=self.bundle.resolve() == output.resolve(),
            )
        return solutions
