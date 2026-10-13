"""Run one or more problems through generation, judging, and optional oracle evaluation."""
from pathlib import Path
import subprocess  # compatibility for callers patching the process runner
from testgen.application.cli import main
from testgen.application.batch_runner import child_cli_args, discover_problem_range
from testgen.application.batch_runner import run_batch as _run_batch

ROOT = Path(__file__).resolve().parent

def run_batch(args, raw_args, parser):
    return _run_batch(args, raw_args, parser, root=ROOT)

if __name__ == "__main__":
    main()
