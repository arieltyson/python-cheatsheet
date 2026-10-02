"""Run every demo_* function: their asserts are the documented results.

Imports only the standard library and snippets/, so it also runs on the
Python 3.10 compatibility job.
"""

import importlib
import inspect
import unittest
from pathlib import Path

SNIPPETS = Path(__file__).resolve().parents[2] / "snippets"


def demo_functions() -> list[tuple[str, object]]:
    demos = []
    for path in sorted(SNIPPETS.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        dotted = ".".join(
            path.relative_to(SNIPPETS.parent).with_suffix("").parts
        )
        module = importlib.import_module(dotted)
        demos.extend(
            (f"{dotted}.{name}", function)
            for name, function in inspect.getmembers(
                module, inspect.isfunction
            )
            if name.startswith("demo_")
            and function.__module__ == dotted
        )
    return demos


class DemoTests(unittest.TestCase):
    def test_every_demo_runs(self) -> None:
        demos = demo_functions()
        self.assertTrue(demos)
        for name, demo in demos:
            with self.subTest(demo=name):
                demo()


if __name__ == "__main__":
    unittest.main()
