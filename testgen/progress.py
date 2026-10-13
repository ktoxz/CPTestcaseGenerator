"""Small, thread-safe console status reporter for long pipeline steps."""

from __future__ import annotations

import sys
import json
import math
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator


class ConsoleProgress:
    def __init__(self, interval_seconds: int = 15):
        self.interval_seconds = interval_seconds
        self._lock = threading.Lock()
        self._latency_path: Path | None = None
        self._latency_events: list[dict] = []

    def bind_latency_log(self, path: Path) -> None:
        """Persist latency events immediately so interrupted runs remain diagnosable."""
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = []
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (isinstance(event, dict)
                        and isinstance(event.get("component"), str)
                        and isinstance(event.get("duration_ms"), (int, float))):
                    existing.append(event)
        with self._lock:
            self._latency_path = path
            self._latency_events.extend(existing)

    def latency(self, component: str, duration_seconds: float, *,
                status: str = "ok", **details) -> dict:
        duration_ms = round(max(0.0, duration_seconds) * 1000, 3)
        event = {
            "timestamp": datetime.now().astimezone().isoformat(timespec="milliseconds"),
            "component": component,
            "duration_ms": duration_ms,
            "status": status,
            **details,
        }
        rendered_details = " ".join(
            f"{key}={json.dumps(value, ensure_ascii=False, separators=(',', ':'))}"
            for key, value in details.items()
        )
        suffix = f" {rendered_details}" if rendered_details else ""
        with self._lock:
            self._latency_events.append(event)
            if self._latency_path is not None:
                with self._latency_path.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            stamp = datetime.now().strftime("%H:%M:%S")
            print(
                f"[{stamp}] LATENCY component={component} duration_ms={duration_ms:.3f} "
                f"status={status}{suffix}",
                file=sys.stderr,
                flush=True,
            )
        return event

    def latency_summary(self) -> dict:
        with self._lock:
            events = list(self._latency_events)
        grouped: dict[str, list[float]] = {}
        for event in events:
            grouped.setdefault(event["component"], []).append(event["duration_ms"])
        components = {}
        for component, values in sorted(grouped.items()):
            ordered = sorted(values)
            p95_index = max(0, math.ceil(len(ordered) * 0.95) - 1)
            components[component] = {
                "count": len(ordered),
                "total_ms": round(sum(ordered), 3),
                "avg_ms": round(sum(ordered) / len(ordered), 3),
                "p50_ms": round(ordered[(len(ordered) - 1) // 2], 3),
                "p95_ms": round(ordered[p95_index], 3),
                "max_ms": round(ordered[-1], 3),
            }
        return {
            "event_count": len(events),
            "components": components,
        }

    def log(self, message: str) -> None:
        with self._lock:
            stamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{stamp}] {message}", file=sys.stderr, flush=True)

    @contextmanager
    def waiting(self, label: str, *, component: str = "stage", **details) -> Iterator[None]:
        started = time.monotonic()
        stopped = threading.Event()
        self.log(f"{label} — bắt đầu")

        def heartbeat() -> None:
            while not stopped.wait(self.interval_seconds):
                self.log(f"{label} — đang chạy ({time.monotonic() - started:.0f}s)")

        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()
        try:
            yield
        except BaseException:
            elapsed = time.monotonic() - started
            self.log(f"{label} — lỗi sau {elapsed:.0f}s")
            self.latency(component, elapsed, status="error", label=label, **details)
            raise
        else:
            elapsed = time.monotonic() - started
            self.log(f"{label} — xong ({elapsed:.0f}s)")
            self.latency(component, elapsed, label=label, **details)
        finally:
            stopped.set()
            thread.join(timeout=1)
