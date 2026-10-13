"""Shared minimum spacing between consecutive outbound LLM prompts."""

from __future__ import annotations

import threading
import time


class EndpointBusyError(RuntimeError):
    """Raised when an earlier timed-out request still occupies an endpoint."""


class EndpointRequestGate:
    """Serialize requests and apply completion/failure cooldowns per endpoint."""

    def __init__(self):
        self._lock = threading.Lock()
        self._in_flight = False
        self._active_lease: int | None = None
        self._next_lease = 0
        self._cooldown_until = 0.0
        self._failure_until = 0.0

    def acquire(self, endpoint: str) -> int:
        while True:
            with self._lock:
                now = time.monotonic()
                if self._in_flight:
                    raise EndpointBusyError(
                        f"Ollama endpoint {endpoint} still has an in-flight "
                        "request; refusing to queue another request"
                    )
                if now < self._failure_until:
                    remaining = self._failure_until - now
                    raise EndpointBusyError(
                        f"Ollama endpoint {endpoint} is cooling down for "
                        f"{remaining:.1f}s after a timeout"
                    )
                remaining = self._cooldown_until - now
                if remaining <= 0:
                    self._in_flight = True
                    self._next_lease += 1
                    self._active_lease = self._next_lease
                    return self._active_lease
            # Normal successful requests leave a deliberate quiet period. Sleep
            # outside the lock so timeout/error bookkeeping remains responsive.
            time.sleep(remaining)

    def complete(self, lease: int, cooldown_seconds: float) -> None:
        with self._lock:
            # A request abandoned at its hard deadline may finish after a newer
            # request has acquired the endpoint. Its stale completion must not
            # release the newer request's lease.
            if self._active_lease != lease:
                return
            self._in_flight = False
            self._active_lease = None
            self._cooldown_until = max(
                self._cooldown_until,
                time.monotonic() + max(0.0, cooldown_seconds),
            )

    def penalize(self, lease: int, cooldown_seconds: float) -> None:
        with self._lock:
            if self._active_lease == lease:
                # The caller has closed the response as far as possible. Do not
                # blacklist the preferred model forever if the daemon HTTP
                # thread itself fails to notice that cancellation.
                self._in_flight = False
                self._active_lease = None
            self._failure_until = max(
                self._failure_until,
                time.monotonic() + max(0.0, cooldown_seconds),
            )

    def reset(self) -> None:
        with self._lock:
            self._in_flight = False
            self._active_lease = None
            self._cooldown_until = 0.0
            self._failure_until = 0.0


_endpoint_gates_lock = threading.Lock()
_endpoint_gates: dict[str, EndpointRequestGate] = {}


def endpoint_request_gate(endpoint: str) -> EndpointRequestGate:
    with _endpoint_gates_lock:
        return _endpoint_gates.setdefault(endpoint.rstrip("/"), EndpointRequestGate())


def reset_endpoint_request_gates() -> None:
    """Test helper; production code should preserve process-wide gate state."""
    with _endpoint_gates_lock:
        for gate in _endpoint_gates.values():
            gate.reset()
        _endpoint_gates.clear()


class PromptThrottle:
    """Enforce a minimum wall-clock gap between the start of consecutive prompts.

    Safe to share across threads: callers running in parallel (e.g. the
    pipeline's judge/LLM worker pools) still queue up and leave at least
    `min_interval_seconds` between any two prompt dispatches, rather than
    firing them back-to-back.
    """

    def __init__(self, min_interval_seconds: float = 0.5):
        if min_interval_seconds < 0:
            raise ValueError("min_interval_seconds must be >= 0")
        self.min_interval_seconds = min_interval_seconds
        self._lock = threading.Lock()
        self._last_dispatch: float | None = None

    def wait(self) -> None:
        """Block, if needed, so this call starts >= min_interval after the last."""
        with self._lock:
            now = time.monotonic()
            if self._last_dispatch is not None:
                remaining = (
                    self._last_dispatch + self.min_interval_seconds - now
                )
                if remaining > 0:
                    time.sleep(remaining)
                    now = time.monotonic()
            self._last_dispatch = now


# One process-wide gap across every LLM backend, so prompts never fire
# back-to-back even when different clients (primary/fallback) are involved.
default_prompt_throttle = PromptThrottle(0.75)
