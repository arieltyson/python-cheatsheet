"""Extract the exact source of a snippet function or class."""

import ast
import textwrap
from pathlib import Path

from tools.manifest import CodeRef


class SnippetNotFoundError(LookupError):
    """Raised when a manifest code ref names a missing definition."""


def extract(snippets_root: Path, ref: CodeRef) -> str:
    """Return a definition's source, or a demo function's body only."""
    source = (snippets_root / ref.path).read_text(encoding="utf-8")
    node = _find_definition(ast.parse(source), ref)
    lines = source.splitlines()
    if not ref.is_demo:
        first_line = min(
            [node.lineno, *(d.lineno for d in node.decorator_list)]
        )
        return "\n".join(lines[first_line - 1 : node.end_lineno])

    # Demos take no arguments, so the def header is one line. Starting
    # right after it keeps comments that precede the first statement.
    first_statement = node.body[0]
    start = (
        first_statement.end_lineno
        if _is_docstring(first_statement)
        else node.lineno
    )
    body_lines = lines[start : node.end_lineno]
    return textwrap.dedent("\n".join(body_lines)).strip("\n")


def _find_definition(
    module: ast.Module, ref: CodeRef
) -> ast.FunctionDef | ast.ClassDef:
    for node in module.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.name == ref.name
        ):
            return node
    raise SnippetNotFoundError(
        f"{ref.path} has no top-level {ref.name}"
    )


def _is_docstring(statement: ast.stmt) -> bool:
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and isinstance(statement.value.value, str)
    )
