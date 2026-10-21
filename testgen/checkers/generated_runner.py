"""Isolated subprocess entry point for an untrusted generated checker."""

from __future__ import annotations

import contextlib
import io
import json
import runpy
import sys


def main() -> int:
    if len(sys.argv) != 3:
        return 2
    script, function = sys.argv[1:]
    request = json.loads(sys.stdin.read())
    # Generated checker prints must never corrupt the protocol response.
    with contextlib.redirect_stdout(io.StringIO()), \
            contextlib.redirect_stderr(io.StringIO()):
        namespace = runpy.run_path(script, run_name="generated_checker")
        callback = namespace.get(function)
        if not callable(callback):
            raise TypeError(f"missing callable {function!r}")
        accepted = callback(
            request["input"], request["actual"], request["expected"]
        )
    sys.stdout.write(json.dumps({"accepted": accepted is True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
