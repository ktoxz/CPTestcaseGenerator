import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RuntimeEnvironmentTests(unittest.TestCase):
    def test_main_image_installs_common_contest_libraries(self):
        dockerfile = (ROOT / "docker" / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("python3-numpy", dockerfile)
        self.assertIn("python3-numba", dockerfile)
        self.assertIn("libboost-all-dev", dockerfile)

    def test_cpp20_and_container_aware_java_heap_are_configured(self):
        catalog = json.loads((ROOT / "config" / "runtimes.json").read_text(encoding="utf-8"))
        runtimes = {runtime["id"]: runtime for runtime in catalog["runtimes"]}
        self.assertIn("-std=gnu++20", runtimes["cpp20"]["compile"])
        self.assertIn("C++20", runtimes["cpp20"]["dialects"])
        self.assertIn("MaxRAMPercentage", runtimes["java"]["execute"])
        self.assertNotIn("-Xmx192m", runtimes["java"]["execute"])
        self.assertIn("numba.pycc", runtimes["python3"]["compile"])
        self.assertIn("ONLINE_JUDGE", runtimes["python3"]["compile"])
        self.assertEqual(runtimes["python3"]["execute"], "cd /work && python3 -s main.py")


if __name__ == "__main__":
    unittest.main()
