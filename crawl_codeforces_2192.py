#!/usr/bin/env python3
"""Download public statements and AC/WA source submissions for Codeforces 2192.

Uses the public Codeforces API for submission metadata and public contest
submission pages for source code. Requests are spaced out to avoid stressing
Codeforces. The run is resumable: completed submission IDs are kept in JSONL.

Usage:
    python crawl_codeforces_2192.py --out cf2192_data

The output directory contains statements.json and submissions.jsonl.
Requires Python 3.9+ and only the standard library.
"""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import random
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CONTEST_ID = 2192
BASE = "https://codeforces.com"
USER_AGENT = "Mozilla/5.0 (compatible; educational-contest-corpus/1.0)"
PAUSE_SECONDS = 2.2
PAGE_SIZE = 1000


def get_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=40) as response:
        return response.read().decode("utf-8", errors="replace")


def pause() -> None:
    time.sleep(PAUSE_SECONDS + random.uniform(0.0, 0.25))


class SourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_source = False
        self.source: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "pre" and dict(attrs).get("id") == "program-source-text":
            self.in_source = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.in_source:
            self.in_source = False

    def handle_data(self, data: str) -> None:
        if self.in_source:
            self.source.append(data)


class StatementParser(HTMLParser):
    """Extract readable text inside Codeforces' problem-statement container."""

    BLOCKS = {"p", "div", "h1", "h2", "h3", "li", "ul", "ol", "pre", "table", "tr"}

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
            if tag in self.BLOCKS:
                self.parts.append("\n")
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.depth:
            self.depth -= 1
            if self.depth and tag in self.BLOCKS:
                self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(part.split()) for part in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line).strip()


def api_submissions() -> list[dict[str, Any]]:
    all_rows: list[dict[str, Any]] = []
    start = 1
    while True:
        query = urlencode({"contestId": CONTEST_ID, "from": start, "count": PAGE_SIZE})
        url = f"{BASE}/api/contest.status?{query}"
        for attempt in range(5):
            try:
                payload = json.loads(get_text(url))
                if payload.get("status") != "OK":
                    raise RuntimeError(f"Codeforces API: {payload.get('comment', 'unknown error')}")
                rows = payload.get("result", [])
                break
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
                if attempt == 4:
                    raise RuntimeError(f"Unable to fetch submission metadata at offset {start}: {exc}") from exc
                wait = min(60, 5 * (attempt + 1))
                print(f"Metadata request failed ({exc}); retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
        all_rows.extend(rows)
        print(f"Fetched metadata: {len(all_rows)} submissions", file=sys.stderr)
        if len(rows) < PAGE_SIZE:
            return all_rows
        start += len(rows)
        pause()


def fetch_statements(out_dir: Path, indices: list[str]) -> None:
    target = out_dir / "statements.json"
    existing: dict[str, Any] = {}
    if target.exists():
        try:
            existing = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    for index in indices:
        if index in existing and existing[index].get("statement"):
            continue
        url = f"{BASE}/contest/{CONTEST_ID}/problem/{index}"
        page = get_text(url)
        parser = StatementParser()
        parser.feed(page)
        statement = parser.text()
        if not statement:
            raise RuntimeError(f"Could not extract statement {index}; raw page was not saved")
        existing[index] = {"contest_id": CONTEST_ID, "index": index, "url": url, "statement": statement}
        target.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved statement {index}", file=sys.stderr)
        pause()


def load_done(path: Path) -> set[int]:
    done: set[int] = set()
    if not path.exists():
        return done
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                done.add(int(json.loads(line)["submission_id"]))
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
    return done


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("--out", type=Path, default=Path("cf2192_data"), help="output directory")
    argp.add_argument("--problems", default="A,B,C,D,E,F", help="comma-separated problem indices")
    argp.add_argument("--limit", type=int, default=0, help="optional cap on AC/WA records for a trial run")
    args = argp.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    indices = [item.strip() for item in args.problems.split(",") if item.strip()]
    fetch_statements(args.out, indices)

    rows = api_submissions()
    keep = [
        row for row in rows
        if row.get("problem", {}).get("contestId") == CONTEST_ID
        and row.get("problem", {}).get("index") in indices
        and row.get("verdict") in {"OK", "WRONG_ANSWER"}
        and row.get("author", {}).get("members")
    ]
    keep.sort(key=lambda row: row["id"])
    if args.limit > 0:
        keep = keep[:args.limit]

    output = args.out / "submissions.jsonl"
    done = load_done(output)
    print(f"Need source for {sum(1 for r in keep if r['id'] not in done)} AC/WA submissions", file=sys.stderr)
    with output.open("a", encoding="utf-8", buffering=1) as stream:
        for number, row in enumerate(keep, 1):
            submission_id = int(row["id"])
            if submission_id in done:
                continue
            problem = row["problem"]
            handle = row["author"]["members"][0].get("handle", "")
            verdict = row["verdict"]
            url = f"{BASE}/contest/{CONTEST_ID}/submission/{submission_id}"
            try:
                page = get_text(url)
                parser = SourceParser()
                parser.feed(page)
                source = "".join(parser.source)
                if not source:
                    raise RuntimeError("source block not found (may be hidden or page structure changed)")
                item = {
                    "contest_id": CONTEST_ID,
                    "submission_id": submission_id,
                    "handle": handle,
                    "problem_index": problem.get("index"),
                    "problem_name": problem.get("name"),
                    "verdict": verdict,
                    "language": row.get("programmingLanguage"),
                    "submitted_at": row.get("creationTimeSeconds"),
                    "time_ms": row.get("timeConsumedMillis"),
                    "memory_bytes": row.get("memoryConsumedBytes"),
                    "url": url,
                    "source_code": source,
                }
                stream.write(json.dumps(item, ensure_ascii=False) + "\n")
                done.add(submission_id)
            except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
                print(f"Skipped submission {submission_id}: {exc}", file=sys.stderr)
            if number % 25 == 0:
                print(f"Processed {number}/{len(keep)} candidates", file=sys.stderr)
            pause()
    print(f"Done. Output: {output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
