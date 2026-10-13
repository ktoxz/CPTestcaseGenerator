#!/usr/bin/env python3
"""Build a bounded, reproducible Codeforces source-code dataset.

For every requested problem, this script downloads the public statement and a
fixed number of accepted/non-accepted submissions.  Submission metadata comes
from the official Codeforces API.  Source code is fetched through the same
authenticated ``/data/submitSource`` request used by the standings popup,
because Codeforces currently rejects anonymous submission-page scraping.

The output is compatible with this repository's local oracle bundle format:

    data/problems/cf<contest><index>/statement.md
    data/problems/cf<contest><index>/oracle/manifest.json
    data/problems/cf<contest><index>/oracle/provenance.json
    data/problems/cf<contest><index>/oracle/sources/{Accepted,WrongAnswer}/

Runs are resumable.  Existing valid manifest entries and source files are kept.
C++ submissions are selected by default.  The exact Codeforces compiler
label is retained in the manifest; the repository-facing dialect is C++17
because the simple contest solutions are expected to be compatible with it.
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import random
import re
import shutil
import sys
import time
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://codeforces.com"
USER_AGENT = "Mozilla/5.0 (compatible; academic-testcase-research/1.0)"
FINAL_NON_AC_VERDICTS = {
    "FAILED",
    "PARTIAL",
    "COMPILATION_ERROR",
    "RUNTIME_ERROR",
    "WRONG_ANSWER",
    "PRESENTATION_ERROR",
    "TIME_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "IDLENESS_LIMIT_EXCEEDED",
    "SECURITY_VIOLATED",
    "CRASHED",
    "INPUT_PREPARATION_CRASHED",
    "CHALLENGED",
}
DEFAULT_PARTICIPANT_TYPES = {"CONTESTANT", "OUT_OF_COMPETITION"}


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def get_text(url: str, attempts: int = 6) -> str:
    for attempt in range(attempts):
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )
            with urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            if attempt + 1 == attempts:
                raise
            wait = min(45.0, 3.0 * (attempt + 1)) + random.uniform(0.0, 0.5)
            log(f"Request failed ({exc}); retrying in {wait:.1f}s: {url}")
            time.sleep(wait)
    raise AssertionError("unreachable")


def polite_pause(seconds: float) -> None:
    time.sleep(seconds + random.uniform(0.0, 0.25))


class SourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_source = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "pre" and dict(attrs).get("id") == "program-source-text":
            self.in_source = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.in_source:
            self.in_source = False

    def handle_data(self, data: str) -> None:
        if self.in_source:
            self.parts.append(data)


class SourceFetcher(Protocol):
    def get(self, submission_id: int) -> str: ...

    def close(self) -> None: ...


class HttpSourceFetcher:
    """Legacy anonymous fetcher retained for old contests/mirrors."""

    def __init__(self, contest_id: int):
        self.contest_id = contest_id

    def get(self, submission_id: int) -> str:
        page = get_text(
            f"{BASE_URL}/contest/{self.contest_id}/submission/{submission_id}"
        )
        parser = SourceParser()
        parser.feed(page)
        source = "".join(parser.parts)
        if not source.strip():
            raise RuntimeError("source block not found")
        return source

    def close(self) -> None:
        return None


class BrowserSourceFetcher:
    """Fetch sources with the logged-in browser session used by standings."""

    def __init__(
        self,
        contest_id: int,
        profile: Path,
        channel: str,
        headless: bool,
        login_prompt: bool,
    ):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Browser mode needs Playwright. Install it with: "
                "python -m pip install playwright"
            ) from exc

        profile.mkdir(parents=True, exist_ok=True)
        self._playwright = sync_playwright().start()
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile.resolve()),
            channel=channel,
            headless=headless,
            viewport=None,
        )
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()
        self._standings_url = f"{BASE_URL}/contest/{contest_id}/standings"
        self._page.goto(self._standings_url, wait_until="domcontentloaded", timeout=60_000)

        logged_in = self._page.locator('a[href*="/logout"]').count() > 0
        if not logged_in and login_prompt and not headless:
            log("Đăng nhập Codeforces trong cửa sổ Chrome vừa mở.")
            try:
                input("Sau khi standings hiện đầy đủ, nhấn Enter để tiếp tục... ")
            except EOFError as exc:
                raise RuntimeError(
                    "Browser chưa đăng nhập và tiến trình không có terminal tương tác"
                ) from exc
            self._page.goto(
                self._standings_url, wait_until="domcontentloaded", timeout=60_000
            )

    def get(self, submission_id: int) -> str:
        response = self._context.request.post(
            f"{BASE_URL}/data/submitSource",
            form={"submissionId": str(submission_id)},
            headers={
                "Referer": self._standings_url,
                "X-Requested-With": "XMLHttpRequest",
            },
            timeout=45_000,
        )
        if not response.ok:
            raise RuntimeError(f"submitSource HTTP {response.status}")
        try:
            payload = response.json()
        except Exception as exc:
            raise RuntimeError("submitSource did not return JSON") from exc
        source = payload.get("source") if isinstance(payload, dict) else None
        if not isinstance(source, str) or not source.strip():
            message = payload.get("error") if isinstance(payload, dict) else None
            raise RuntimeError(f"source unavailable{': ' + str(message) if message else ''}")
        return source

    def close(self) -> None:
        self._context.close()
        self._playwright.stop()


class StatementParser(HTMLParser):
    """Extract readable text from the English problem-statement container."""

    BLOCK_TAGS = {
        "div", "p", "pre", "li", "ul", "ol", "table", "tr", "h1", "h2", "h3"
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        if self.depth == 0 and "problem-statement" in classes:
            self.depth = 1
            return
        if self.depth:
            if tag in self.BLOCK_TAGS:
                self.parts.append("\n")
            self.depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.depth and tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self.depth:
            self.depth -= 1
            if self.depth and tag in self.BLOCK_TAGS:
                self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line).strip()


def api_page(contest_id: int, start: int, count: int) -> list[dict[str, Any]]:
    query = urlencode({"contestId": contest_id, "from": start, "count": count})
    payload = json.loads(get_text(f"{BASE_URL}/api/contest.status?{query}"))
    if payload.get("status") != "OK":
        raise RuntimeError(f"Codeforces API error: {payload.get('comment', 'unknown error')}")
    return payload.get("result", [])


def enough_candidates(
    buckets: dict[tuple[str, str], list[dict[str, Any]]],
    problems: list[str],
    target: int,
) -> bool:
    # Extra metadata candidates absorb duplicate source, duplicate author, and
    # occasional source pages that Codeforces refuses to serve.
    reserve = max(target * 3, target + 20)
    return all(len(buckets[(index, group)]) >= reserve for index in problems for group in ("ac", "nonac"))


def fetch_candidates(
    contest_id: int,
    problems: list[str],
    target: int,
    language: str,
    page_size: int,
    max_pages: int,
    pause: float,
    participant_types: set[str],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    buckets = {(index, group): [] for index in problems for group in ("ac", "nonac")}
    start = 1
    for page_number in range(1, max_pages + 1):
        rows = api_page(contest_id, start, page_size)
        log(f"Metadata page {page_number}: {len(rows)} rows (offset {start})")
        for row in rows:
            problem = row.get("problem", {})
            index = str(problem.get("index", ""))
            verdict = row.get("verdict")
            members = row.get("author", {}).get("members") or []
            participant_type = str(row.get("author", {}).get("participantType", ""))
            row_language = str(row.get("programmingLanguage", ""))
            if (
                index not in problems
                or language not in row_language
                or not members
                or participant_type not in participant_types
                or verdict not in ({"OK"} | FINAL_NON_AC_VERDICTS)
            ):
                continue
            group = "ac" if verdict == "OK" else "nonac"
            buckets[(index, group)].append(row)
        if enough_candidates(buckets, problems, target):
            break
        if len(rows) < page_size:
            break
        start += len(rows)
        polite_pause(pause)

    missing = {
        f"{index}/{group}": len(buckets[(index, group)])
        for index in problems
        for group in ("ac", "nonac")
        if len(buckets[(index, group)]) < target
    }
    if missing:
        raise RuntimeError(f"Not enough metadata candidates for requested quota: {missing}")
    return buckets


def statement_markdown(contest_id: int, index: str) -> tuple[str, str]:
    url = f"{BASE_URL}/contest/{contest_id}/problem/{index}"
    page = get_text(url)
    parser = StatementParser()
    parser.feed(page)
    body = html.unescape(parser.text())
    if not body:
        raise RuntimeError(f"Could not extract statement for problem {index}")
    title_match = re.search(r'<div class="title">\s*([^<]+)', page)
    title = html.unescape(title_match.group(1)).strip() if title_match else f"Problem {index}"
    header = f"# {title}\n\nSource: {url}\n\n"
    return header + body + "\n", title


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_existing(oracle_dir: Path, problem_id: str) -> list[dict[str, Any]]:
    path = oracle_dir / "manifest.json"
    if not path.exists():
        return []
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    valid = []
    for row in rows:
        source = oracle_dir / str(row.get("source", ""))
        if (
            row.get("problem_id") == problem_id
            and source.is_file()
            and sha256_bytes(source.read_bytes()) == row.get("sha256")
        ):
            valid.append(row)
    return valid


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_problem(
    contest_id: int,
    index: str,
    candidates: dict[tuple[str, str], list[dict[str, Any]]],
    problems_root: Path,
    target: int,
    pause: float,
    source_fetcher: SourceFetcher,
) -> None:
    problem_id = f"cf{contest_id}{index.lower()}"
    problem_dir = problems_root / problem_id
    oracle_dir = problem_dir / "oracle"
    accepted_dir = oracle_dir / "sources" / "Accepted"
    nonac_dir = oracle_dir / "sources" / "WrongAnswer"
    accepted_dir.mkdir(parents=True, exist_ok=True)
    nonac_dir.mkdir(parents=True, exist_ok=True)

    statement_path = problem_dir / "statement.md"
    metadata_path = problem_dir / "metadata.json"
    if not statement_path.exists():
        statement, title = statement_markdown(contest_id, index)
        statement_path.write_text(statement, encoding="utf-8")
        write_json(metadata_path, {
            "problem_id": problem_id,
            "contest_id": contest_id,
            "index": index,
            "title": title,
            "url": f"{BASE_URL}/contest/{contest_id}/problem/{index}",
        })
        polite_pause(pause)

    entries = load_existing(oracle_dir, problem_id)
    provenance_by_id: dict[str, dict[str, Any]] = {}
    provenance_path = oracle_dir / "provenance.json"
    if provenance_path.exists():
        try:
            existing_provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            provenance_by_id = {row["id"]: row for row in existing_provenance.get("sources", [])}
        except (json.JSONDecodeError, KeyError, TypeError):
            provenance_by_id = {}

    for group, label, directory, short_id in (
        ("ac", "Accepted", accepted_dir, "ac"),
        ("nonac", "Wrong Answer", nonac_dir, "nonac"),
    ):
        group_entries = [row for row in entries if row.get("label") == label]
        used_handles = {str(row.get("handle", "")).lower() for row in group_entries}
        used_hashes = {row["sha256"] for row in group_entries}
        used_submission_ids = {row.get("submission_id") for row in group_entries}
        log(f"{problem_id} {group}: resume at {len(group_entries)}/{target}")

        for row in candidates[(index, group)]:
            if len(group_entries) >= target:
                break
            submission_id = int(row["id"])
            handle = str(row["author"]["members"][0].get("handle", ""))
            if submission_id in used_submission_ids or handle.lower() in used_handles:
                continue
            url = f"{BASE_URL}/contest/{contest_id}/submission/{submission_id}"
            try:
                source = source_fetcher.get(submission_id)
                source = source.replace("\r\n", "\n").replace("\r", "\n")
                if not source.endswith("\n"):
                    source += "\n"
                content = source.encode("utf-8")
                digest = sha256_bytes(content)
                if digest in used_hashes:
                    continue

                ordinal = len(group_entries) + 1
                relative = f"sources/{directory.name}/{ordinal}.cpp"
                source_path = oracle_dir / relative
                source_path.write_bytes(content)
                item_id = f"{problem_id}-{short_id}-{ordinal:02d}"
                item = {
                    "id": item_id,
                    "problem_id": problem_id,
                    "label": label,
                    "verdict": row.get("verdict"),
                    "language": "C++",
                    "dialect": "C++17",
                    "codeforces_language": row.get("programmingLanguage"),
                    "source": relative,
                    "sha256": digest,
                    "contest_id": contest_id,
                    "problem_index": index,
                    "submission_id": submission_id,
                    "handle": handle,
                    "submitted_at": row.get("creationTimeSeconds"),
                    "time_ms": row.get("timeConsumedMillis"),
                    "memory_bytes": row.get("memoryConsumedBytes"),
                    "url": url,
                }
                group_entries.append(item)
                entries.append(item)
                used_handles.add(handle.lower())
                used_hashes.add(digest)
                used_submission_ids.add(submission_id)
                provenance_by_id[item_id] = {
                    "id": item_id,
                    "submission_id": submission_id,
                    "handle": handle,
                    "verdict": row.get("verdict"),
                    "url": url,
                    "copied_as": relative,
                    "sha256": digest,
                    "language": "C++",
                    "dialect": "C++17",
                    "codeforces_language": row.get("programmingLanguage"),
                    "label": label,
                }
                entries.sort(key=lambda entry: entry["id"])
                write_json(oracle_dir / "manifest.json", entries)
                write_json(provenance_path, {
                    "problem_id": problem_id,
                    "source": "Public Codeforces contest submissions",
                    "selection_policy": (
                        "Newest unique-author, unique-source C++ submissions; "
                        "20 OK and 20 final non-OK verdicts"
                    ),
                    "sources": sorted(provenance_by_id.values(), key=lambda item: item["id"]),
                })
                log(f"{problem_id} {group}: {len(group_entries)}/{target} (submission {submission_id})")
            except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
                log(f"Skip submission {submission_id}: {exc}")
            polite_pause(pause)

        if len(group_entries) < target:
            raise RuntimeError(
                f"Only downloaded {len(group_entries)}/{target} sources for {problem_id}/{group}"
            )


def build_summary(contest_id: int, problems: list[str], root: Path, target: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "contest_id": contest_id,
        "contest_url": f"{BASE_URL}/contest/{contest_id}",
        "per_problem": {"accepted": target, "non_accepted": target},
        "problems": {},
    }
    for index in problems:
        problem_id = f"cf{contest_id}{index.lower()}"
        manifest = json.loads(
            (root / problem_id / "oracle" / "manifest.json").read_text(encoding="utf-8")
        )
        verdicts: dict[str, int] = {}
        for row in manifest:
            verdict = row.get("verdict", "UNKNOWN")
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
        result["problems"][index] = {
            "problem_id": problem_id,
            "accepted": sum(row["label"] == "Accepted" for row in manifest),
            "non_accepted": sum(row["label"] == "Wrong Answer" for row in manifest),
            "verdicts": dict(sorted(verdicts.items())),
            "directory": str((root / problem_id).resolve()),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contest", type=int, required=True)
    parser.add_argument("--problems", default="A,B,C,D,E,F,G")
    parser.add_argument("--per-label", type=int, default=20)
    parser.add_argument(
        "--language",
        default="C++17",
        help="programmingLanguage substring (default: C++17)",
    )
    parser.add_argument("--problems-root", type=Path, default=Path("data/problems"))
    parser.add_argument("--page-size", type=int, default=10000)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--pause", type=float, default=1.1)
    parser.add_argument("--zip", type=Path, default=None)
    parser.add_argument(
        "--source-mode", choices=("browser", "http"), default="browser",
        help="browser uses the authenticated standings source endpoint (default)",
    )
    parser.add_argument(
        "--browser-profile", type=Path, default=Path(".codeforces-browser"),
        help="persistent Chrome profile; login is remembered between runs",
    )
    parser.add_argument("--browser-channel", default="chrome")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--no-login-prompt", action="store_true",
        help="fail instead of waiting for interactive browser login",
    )
    parser.add_argument(
        "--participant-types", default="CONTESTANT,OUT_OF_COMPETITION",
        help="comma-separated Codeforces participant types; PRACTICE is excluded by default",
    )
    parser.add_argument(
        "--statements-only",
        action="store_true",
        help="download public statements and metadata without submission sources",
    )
    args = parser.parse_args()

    problems = [item.strip().upper() for item in args.problems.split(",") if item.strip()]
    participant_types = {
        item.strip().upper()
        for item in args.participant_types.split(",")
        if item.strip()
    }
    if args.per_label < 1:
        parser.error("--per-label must be positive")
    args.problems_root.mkdir(parents=True, exist_ok=True)

    if args.statements_only:
        for index in problems:
            problem_id = f"cf{args.contest}{index.lower()}"
            problem_dir = args.problems_root / problem_id
            problem_dir.mkdir(parents=True, exist_ok=True)
            statement_path = problem_dir / "statement.md"
            metadata_path = problem_dir / "metadata.json"
            if statement_path.exists() and metadata_path.exists():
                log(f"{problem_id}: statement already present")
                continue
            statement, title = statement_markdown(args.contest, index)
            statement_path.write_text(statement, encoding="utf-8")
            write_json(metadata_path, {
                "problem_id": problem_id,
                "contest_id": args.contest,
                "index": index,
                "title": title,
                "url": f"{BASE_URL}/contest/{args.contest}/problem/{index}",
            })
            log(f"{problem_id}: saved statement")
            polite_pause(args.pause)
        return 0

    candidates = fetch_candidates(
        args.contest,
        problems,
        args.per_label,
        args.language,
        args.page_size,
        args.max_pages,
        args.pause,
        participant_types,
    )
    source_fetcher: SourceFetcher
    if args.source_mode == "browser":
        source_fetcher = BrowserSourceFetcher(
            args.contest,
            args.browser_profile,
            args.browser_channel,
            args.headless,
            not args.no_login_prompt,
        )
    else:
        source_fetcher = HttpSourceFetcher(args.contest)
    try:
        for index in problems:
            save_problem(
                args.contest,
                index,
                candidates,
                args.problems_root,
                args.per_label,
                args.pause,
                source_fetcher,
            )
    finally:
        source_fetcher.close()

    summary = build_summary(args.contest, problems, args.problems_root, args.per_label)
    summary_path = args.problems_root / f"cf{args.contest}_dataset_summary.json"
    write_json(summary_path, summary)
    log(f"Wrote summary: {summary_path}")

    if args.zip is not None:
        args.zip.parent.mkdir(parents=True, exist_ok=True)
        staging = args.problems_root / f"cf{args.contest}_dataset"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir()
        for index in problems:
            problem_id = f"cf{args.contest}{index.lower()}"
            shutil.copytree(args.problems_root / problem_id, staging / problem_id)
        shutil.copy2(summary_path, staging / summary_path.name)
        archive_base = args.zip.with_suffix("")
        archive = Path(shutil.make_archive(str(archive_base), "zip", staging.parent, staging.name))
        shutil.rmtree(staging)
        log(f"Wrote archive: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
