"""Content rules that keep every snippet interview-ready."""

import ast
import unittest
from pathlib import Path

from tools.build import MANIFEST, SNIPPETS
from tools.manifest import load_site
from tools.source import extract

ALLOWED_IMPORTS = {"collections", "heapq", "math"}
MAX_LINE_LENGTH = 72
MAX_FUNCTION_LINES = 25


def snippet_files() -> list[Path]:
    return sorted(
        path
        for path in SNIPPETS.rglob("*.py")
        if path.name != "__init__.py"
    )


def imported_modules(module: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add("." * node.level + (node.module or ""))
    return names


class SnippetRulesTests(unittest.TestCase):
    def test_snippets_exist(self) -> None:
        self.assertTrue(snippet_files())

    def test_imports_stay_on_the_allowlist(self) -> None:
        for path in snippet_files():
            module = ast.parse(path.read_text(encoding="utf-8"))
            for name in imported_modules(module):
                with self.subTest(file=path.name, module=name):
                    self.assertIn(name.split(".")[0], ALLOWED_IMPORTS)

    def test_lines_fit_a_half_width_window(self) -> None:
        for path in snippet_files():
            lines = path.read_text(encoding="utf-8").splitlines()
            for number, line in enumerate(lines, start=1):
                with self.subTest(file=path.name, line=number):
                    self.assertLessEqual(len(line), MAX_LINE_LENGTH)

    def test_functions_fit_one_glance(self) -> None:
        for path in snippet_files():
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.FunctionDef):
                    length = node.end_lineno - node.lineno + 1
                    with self.subTest(file=path.name, name=node.name):
                        self.assertLessEqual(length, MAX_FUNCTION_LINES)


class ManifestCoverageTests(unittest.TestCase):
    def test_every_code_ref_resolves(self) -> None:
        for entry in load_site(MANIFEST, SNIPPETS).entries():
            for ref in entry.code:
                with self.subTest(entry=entry.id, ref=ref.name):
                    self.assertTrue(extract(SNIPPETS, ref).strip())

    def test_every_public_definition_is_on_the_page(self) -> None:
        shown = {
            (ref.path, ref.name)
            for entry in load_site(MANIFEST, SNIPPETS).entries()
            for ref in entry.code
        }
        for path in snippet_files():
            relative = path.relative_to(SNIPPETS).as_posix()
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in module.body:
                is_definition = isinstance(
                    node, (ast.FunctionDef, ast.ClassDef)
                )
                if is_definition and not node.name.startswith("_"):
                    self.assertTrue(
                        (relative, node.name) in shown,
                        f"{relative}:{node.name} is not in site.toml",
                    )


if __name__ == "__main__":
    unittest.main()
