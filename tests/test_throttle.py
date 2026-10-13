from __future__ import annotations

import time
import unittest

from testgen.throttle import EndpointRequestGate


class EndpointRequestGateTests(unittest.TestCase):
    def test_successful_request_leaves_post_completion_quiet_period(self) -> None:
        gate = EndpointRequestGate()
        lease = gate.acquire("http://ollama.test")
        gate.complete(lease, 0.05)

        started = time.monotonic()
        lease = gate.acquire("http://ollama.test")
        elapsed = time.monotonic() - started
        gate.complete(lease, 0)

        self.assertGreaterEqual(elapsed, 0.04)
        self.assertLess(elapsed, 0.5)

    def test_timeout_allows_preferred_endpoint_again_after_cooldown(self) -> None:
        gate = EndpointRequestGate()
        stale_lease = gate.acquire("http://ollama.test")
        gate.penalize(stale_lease, 0.02)

        with self.assertRaisesRegex(RuntimeError, "cooling down"):
            gate.acquire("http://ollama.test")
        time.sleep(0.03)
        current_lease = gate.acquire("http://ollama.test")

        # A late completion from the abandoned request must not release the
        # current request.
        gate.complete(stale_lease, 0)
        with self.assertRaisesRegex(RuntimeError, "in-flight"):
            gate.acquire("http://ollama.test")
        gate.complete(current_lease, 0)


if __name__ == "__main__":
    unittest.main()
