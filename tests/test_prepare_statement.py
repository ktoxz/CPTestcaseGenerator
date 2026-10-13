from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_statement import (
    prepare_problem,
    split_statement,
    strip_outer_fence,
    validate_translation,
)


ENGLISH = """# Sum

- CodeNet ID: `p00001`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Add two integers.

## Input

```text
1 2
```

## Output

```text
3
```
"""

JAPANESE = """# 和

二つの整数を足してください。これは入力された値の和を求める問題です。

## 入力

```text
1 2
```

## 出力

```text
3
```
"""

TRANSLATED = """Add two integers and print their sum. The input contains two integer values.
Both values are provided on one line, separated by a space. Compute the exact
integer sum and print that value on its own line. Do not print any additional
text before or after the answer.

## Input

```text
1 2
```

## Output

```text
3
```
"""


class PrepareStatementTests(unittest.TestCase):
    def test_strip_json_fence_from_ollama(self) -> None:
        self.assertEqual(strip_outer_fence('```json\n{"title":"Sum"}\n```'),
                         '{"title":"Sum"}')

    def test_split_statement_metadata(self) -> None:
        title, body, metadata = split_statement(ENGLISH)
        self.assertEqual(title, "Sum")
        self.assertEqual(metadata["problem_id"], "p00001")
        self.assertEqual(metadata["time_limit_ms"], "1000")
        self.assertTrue(body.startswith("Add two integers."))

    def test_prepare_english_without_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "p00001" / "statement.md"
            source.parent.mkdir()
            source.write_text(ENGLISH, encoding="utf-8")
            output = root / "output" / "p00001"
            result = prepare_problem(source, output, translate_mode="auto")
            self.assertFalse(result["translated"])
            self.assertFalse((output / "statement.original.md").exists())
            prepared = (output / "statement.md").read_text(encoding="utf-8")
            self.assertIn("- CodeNet ID: `p00001`", prepared)
            metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
            self.assertFalse(metadata["translation"]["performed"])

    def test_prepare_translation_and_copy_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "p00002" / "statement.md"
            source.parent.mkdir()
            source.write_text(JAPANESE + "\n![diagram](diagram.png)\n", encoding="utf-8")
            (source.parent / "diagram.png").write_bytes(b"png")
            metadata = source.parent / "metadata.json"
            metadata.write_text(json.dumps({
                "problem_id": "p00002", "name": "Wa", "dataset": "AIZU",
                "time_limit_ms": 1000, "memory_limit_kb": 131072,
            }), encoding="utf-8")

            def fake_translator(title, body, source_language, target_language):
                self.assertEqual(source_language, "Japanese")
                return "Sum", TRANSLATED + "\n![diagram](diagram.png)\n"

            output = root / "output" / "p00002"
            result = prepare_problem(source, output, metadata_path=metadata,
                                     translator=fake_translator, translate_mode="auto")
            self.assertTrue(result["translated"])
            self.assertTrue((output / "statement.original.md").is_file())
            self.assertEqual((output / "diagram.png").read_bytes(), b"png")
            prepared = (output / "statement.md").read_text(encoding="utf-8")
            self.assertTrue(prepared.startswith("# Sum\n"))

    def test_reject_changed_sample_block(self) -> None:
        with self.assertRaisesRegex(ValueError, "fenced code block"):
            validate_translation(ENGLISH, TRANSLATED.replace("1 2", "2 2"), "English")


if __name__ == "__main__":
    unittest.main()
