import os
import shutil
import json
import hashlib
from pathlib import Path

problem_dir = Path("d:/KLTN/Final_TestcaseGenerator/data/problems/G1")
problem_dir.mkdir(parents=True, exist_ok=True)

# 1. Statement.md
statement_md = """# G1. Yunli's Subarray Queries (easy version)

Source: https://codeforces.com/contest/2009/problem/G1

G1. Yunli's Subarray Queries (easy version)
time limit per test
3 seconds
memory limit per test
512 megabytes
input
standard input
output
standard output

This is the easy version of the problem. In this version, it is guaranteed that $$$r=l+k-1$$$ for all queries.

For an arbitrary array $$$b$$$, Yunli can perform the following operation any number of times:
Select an index $$$i$$$. Set $$$b_i = x$$$ where $$$x$$$ is any integer she desires ($$$x$$$ is not limited to the interval $$$[1,n]$$$).
Denote $$$f(b)$$$ as the minimum number of operations she needs to perform until there exists a consecutive subarray$$$^{\\text{∗}}$$$ of length at least $$$k$$$ in $$$b$$$.

Yunli is given an array $$$a$$$ of size $$$n$$$ and asks you $$$q$$$ queries. In each query, you must output $$$\\sum_{j=l+k-1}^{r} f([a_l, a_{l+1}, \\ldots, a_j])$$$ . Note that in this version, you are only required to output $$$f([a_l, a_{l+1}, \\ldots, a_{l+k-1}])$$$ .

$$$^{\\text{∗}}$$$ If there exists a consecutive subarray of length $$$k$$$ that starts at index $$$i$$$ ($$$1 \\leq i \\leq |b|-k+1$$$), then $$$b_j = b_{j-1} + 1$$$ for all $$$i < j \\leq i+k-1$$$.

Input
The first line contains $$$t$$$ ($$$1 \\leq t \\leq 10^4$$$) — the number of test cases.

The first line of each test case contains three integers $$$n$$$, $$$k$$$, and $$$q$$$ ($$$1 \\leq k \\leq n \\leq 2 \\cdot 10^5$$$, $$$1 \\leq q \\leq 2 \\cdot 10^5$$$) — the length of the array, the length of the consecutive subarray, and the number of queries.

The following line contains $$$n$$$ integers $$$a_1, a_2, \\dots, a_n$$$ ($$$1 \\leq a_i \\leq n$$$).

The following $$$q$$$ lines contain two integers $$$l$$$ and $$$r$$$ ($$$1 \\leq l \\leq r \\leq n$$$, $$$r=l+k-1$$$) — the bounds of the query.

It is guaranteed that the sum of $$$n$$$ over all test cases does not exceed $$$2 \\cdot 10^5$$$ and the sum of $$$q$$$ over all test cases does not exceed $$$2 \\cdot 10^5$$$.

Output
Output $$$\\sum_{j=l+k-1}^{r} f([a_l, a_{l+1}, \\ldots, a_j])$$$ for each query on a new line.

## Example

## Sample Input 1
```text
3
7 5 3
1 2 3 2 1 2 3
1 5
2 6
3 7
8 4 2
4 3 1 1 2 4 3 2
3 6
2 5
5 4 2
4 5 1 2 3
1 4
2 5
```

## Output for the Sample Input 1
```text
2
3
2
2
2
2
1
```

Note
In the first query of the first testcase, $$$b=[1,2,3,2,1]$$$. Yunli can make a consecutive subarray of length $$$5$$$ in $$$2$$$ moves:
Set $$$b_4=4$$$, Set $$$b_5=5$$$. After operations $$$b=[1, 2, 3, 4, 5]$$$.
In the second query of the first testcase, $$$b=[2,3,2,1,2]$$$. Yunli can make a consecutive subarray of length $$$5$$$ in $$$3$$$ moves:
Set $$$b_3=0$$$, Set $$$b_2=-1$$$, Set $$$b_1=-2$$$. After operations $$$b=[-2, -1, 0, 1, 2]$$$.
"""

(problem_dir / "statement.md").write_text(statement_md, encoding="utf-8")
print("Wrote statement.md")

# 2. metadata.json
metadata = {
    "problem_id": "G1",
    "contest_id": 2009,
    "index": "G1",
    "title": "G1. Yunli's Subarray Queries (easy version)",
    "url": "https://codeforces.com/contest/2009/problem/G1",
    "time_limit_ms": 3000,
    "memory_limit_mb": 512,
    "samples": [
        {
            "input": "3\n7 5 3\n1 2 3 2 1 2 3\n1 5\n2 6\n3 7\n8 4 2\n4 3 1 1 2 4 3 2\n3 6\n2 5\n5 4 2\n4 5 1 2 3\n1 4\n2 5\n",
            "output": "2\n3\n2\n2\n2\n2\n1\n"
        }
    ]
}
(problem_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Wrote metadata.json")

# 3. checker.json
checker = {"kind": "TOKEN"}
(problem_dir / "checker.json").write_text(json.dumps(checker, indent=2) + "\n", encoding="utf-8")
print("Wrote checker.json")

# 4. Organize oracle folder
oracle_dir = problem_dir / "oracle"
sources_ac = oracle_dir / "sources" / "Accepted"
sources_wa = oracle_dir / "sources" / "WrongAnswer"
sources_ac.mkdir(parents=True, exist_ok=True)
sources_wa.mkdir(parents=True, exist_ok=True)

# Copy from existing Accepted and WrongAnswers
orig_ac = oracle_dir / "Accepted"
orig_wa = oracle_dir / "WrongAnswers"

if orig_ac.is_dir():
    for f in orig_ac.iterdir():
        if f.is_file():
            shutil.copy2(f, sources_ac / f.name)

if orig_wa.is_dir():
    for f in orig_wa.iterdir():
        if f.is_file():
            shutil.copy2(f, sources_wa / f.name)

# 5. Build manifest.json
manifest = []
ac_files = sorted(sources_ac.glob("*.cpp"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.name)
for idx, f in enumerate(ac_files, 1):
    manifest.append({
        "id": f"G1-ac-{idx}",
        "problem_id": "G1",
        "label": "Accepted",
        "language": "C++",
        "dialect": "C++17",
        "source": f"sources/Accepted/{f.name}",
        "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
    })

wa_files = sorted(sources_wa.glob("*.cpp"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.name)
for idx, f in enumerate(wa_files, 1):
    manifest.append({
        "id": f"G1-wa-{idx}",
        "problem_id": "G1",
        "label": "Wrong Answer",
        "language": "C++",
        "dialect": "C++17",
        "source": f"sources/WrongAnswer/{f.name}",
        "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
    })

(oracle_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote oracle/manifest.json with {len(ac_files)} AC and {len(wa_files)} WA sources.")
