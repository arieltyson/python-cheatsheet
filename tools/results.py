"""Show demo asserts as `expression  # result` lines.

The snippet files keep real asserts so the documented results are
executed by the tests. On the page, `assert total == 3` reads as
`total  # 3`, which is shorter and copies as runnable code.
"""

import ast

MAX_LINE_LENGTH = 72
COMMENT_GAP = "  # "


def asserts_as_results(source: str) -> str:
    lines = source.split("\n")
    rewritten: dict[int, tuple[str, str, str]] = {}
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert) or node.msg is not None:
            continue
        if node.lineno != node.end_lineno:
            continue
        line = lines[node.lineno - 1]
        if line[node.end_col_offset :].strip():
            continue
        expression, result = _split_assert(node.test, source)
        indent = line[: node.col_offset]
        rewritten[node.lineno - 1] = (indent, expression, result)

    for run in _consecutive_runs(sorted(rewritten)):
        parts = [rewritten[index] for index in run]
        width = max(len(indent + expr) for indent, expr, _ in parts)
        fits = all(
            width + len(COMMENT_GAP) + len(result) <= MAX_LINE_LENGTH
            for _, _, result in parts
        )
        for index, (indent, expr, result) in zip(
            run, parts, strict=True
        ):
            code = indent + expr
            padded = code.ljust(width) if fits else code
            lines[index] = f"{padded}{COMMENT_GAP}{result}"
    return "\n".join(lines)


def _split_assert(test: ast.expr, source: str) -> tuple[str, str]:
    segment = ast.get_source_segment
    if (
        isinstance(test, ast.Compare)
        and len(test.ops) == 1
        and isinstance(test.ops[0], (ast.Eq, ast.Is))
    ):
        return (
            segment(source, test.left),
            segment(source, test.comparators[0]),
        )
    return segment(source, test), "True"


def _consecutive_runs(indexes: list[int]) -> list[list[int]]:
    runs: list[list[int]] = []
    for index in indexes:
        if runs and runs[-1][-1] == index - 1:
            runs[-1].append(index)
        else:
            runs.append([index])
    return runs
