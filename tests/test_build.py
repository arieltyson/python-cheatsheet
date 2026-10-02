import tempfile
import unittest
from pathlib import Path

from tools.build import build, fill
from tools.manifest import CodeRef
from tools.source import extract

SAMPLE = '''\
def demo_numbers() -> None:
    """Docstring is not shown."""
    # Comments are shown.
    total = sum([1, 2])
    assert total == 3


def add(left: int, right: int) -> int:
    return left + right
'''


class FillTests(unittest.TestCase):
    def test_fills_slots(self) -> None:
        self.assertEqual(fill("a<!-- slot:x -->b", {"x": "1"}), "a1b")

    def test_rejects_unknown_slot(self) -> None:
        with self.assertRaises(KeyError):
            fill("ab", {"x": "1"})

    def test_rejects_unfilled_slot(self) -> None:
        with self.assertRaises(KeyError):
            fill("<!-- slot:x --><!-- slot:y -->", {"x": "1"})


class ExtractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "sample.py").write_text(SAMPLE)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_demo_shows_body_without_docstring(self) -> None:
        code = extract(self.root, CodeRef("sample.py", "demo_numbers"))
        self.assertEqual(
            code.splitlines(),
            [
                "# Comments are shown.",
                "total = sum([1, 2])",
                "assert total == 3",
            ],
        )

    def test_function_shows_whole_definition(self) -> None:
        code = extract(self.root, CodeRef("sample.py", "add"))
        self.assertTrue(code.startswith("def add("))
        self.assertTrue(code.endswith("return left + right"))


class BuildTests(unittest.TestCase):
    def test_build_writes_index(self) -> None:
        with tempfile.TemporaryDirectory() as output:
            index = build(Path(output) / "dist")
            self.assertIn("<main", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
