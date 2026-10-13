"""Smoke-check the local or SSH Docker judge without Ollama."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from testgen.checker import checker_from_profile
from testgen.docker_judge import DockerJudge
from testgen.domain import Solution
from testgen.remote_judge import RemoteDockerJudge
from testgen.progress import ConsoleProgress
from testgen.runtime import RuntimeCatalog


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--judge", choices=("local", "remote"), default="local")
    default_host = json.loads((ROOT / "config" / "judge.json").read_text(encoding="utf-8"))["ssh_host"]
    parser.add_argument("--judge-host", default=default_host)
    args = parser.parse_args()
    progress = ConsoleProgress()
    catalog = RuntimeCatalog()
    build = ROOT / "output" / ("remote-smoke" if args.judge == "remote" else "smoke") / "build"
    if args.judge == "remote":
        with progress.waiting(f"Kiểm tra judge SSH {args.judge_host}"):
            judge = RemoteDockerJudge(build, args.judge_host, catalog)
        for image in catalog.images_to_build(include_oracle=False):
            with progress.waiting(f"Chuẩn bị image {image['tag']} trên KHOI"):
                judge.ensure_images([image], ROOT / "docker")
    else:
        judge = DockerJudge(build, catalog)
    checker = checker_from_profile({"kind": "TOKEN"})
    expected = "2 24\n10000000 150000000\n"
    input_text = "8 6\n50000000 30000000\n"
    for name, label in (("ac", "candidate_ac"), ("wa", "candidate_wa")):
        solution = Solution(name, label, "C++", ROOT / "examples" / f"p00005_{name}.cpp")
        progress.log(f"Biên dịch code mẫu {name}")
        compiled = judge.compile(solution)
        if compiled.verdict != "PASS":
            raise RuntimeError(f"{name} compile failed: {compiled.stderr}")
        progress.log(f"Chấm code mẫu {name}")
        run = judge.execute(solution, "sample", input_text)
        print(name, run.verdict, "PASS" if checker.accepts(run.actual, expected) else "WA", repr(run.actual))
        if run.verdict != "PASS" or checker.accepts(run.actual, expected) != (name == "ac"):
            raise RuntimeError("Unexpected smoke result")
        if args.judge == "remote":
            batch = judge.execute_many(solution, [("first", "8 6\n"),
                                                  ("second", "5 10\n")])
            expected_batch = ["2 24\n", "5 10\n"]
            if len(batch) != 2 or any(
                    result.verdict != "PASS" or
                    checker.accepts(result.actual, expected_text) != (name == "ac")
                    for result, expected_text in zip(batch, expected_batch)):
                raise RuntimeError(f"Unexpected remote batch result: {batch}")
            progress.log(f"Batch SSH {name}: PASS")


if __name__ == "__main__":
    main()
