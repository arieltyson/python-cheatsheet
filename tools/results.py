"""Show demo asserts as `expression  # result` lines.

The snippet files keep real asserts so the documented results are
executed by the tests. On the page, `assert total == 3` reads as
`total  # 3`, which is shorter and copies as runnable code.

Each check gets its own line and its own result: `assert a == 1 and b`
becomes two lines, `assert not x` reads `x  # False`, and a note after
an assert (`assert x  # why`) moves onto its own comment line above.
"""

import ast

MAX_LINE_LENGTH = 72
COMMENT_GAP = "  # "

Result = tuple[str, str, str]


def asserts_as_results(source: str) -> str:
    lines = source.split("\n")
    replacements: dict[int, list[str | Result]] = {}
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert) or node.msg is not None:
            continue
        if node.lineno != node.end_lineno:
            continue
        line = lines[node.lineno - 1]
        trailing = line[node.end_col_offset :].strip()
        if trailing and not trailing.startswith("#"):
            continue
        indent = line[: node.col_offset]
        checks = (
            node.test.values
            if isinstance(node.test, ast.BoolOp)
            and isinstance(node.test.op, ast.And)
            else [node.test]
        )
        rows: list[str | Result] = (
            [f"{indent}{trailing}"] if trailing else []
        )
        for check in checks:
            expression, result = _split_assert(check, source)
            rows.append((indent, expression, result))
        replacements[node.lineno - 1] = rows

    output: list[str | Result] = []
    for index, line in enumerate(lines):
        output.extend(replacements.get(index, [line]))
    return "\n".join(_align(output))


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
    if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
        return segment(source, test.operand), "False"
    return segment(source, test), "True"


def _align(rows: list[str | Result]) -> list[str]:
    lines: list[str] = []
    run: list[Result] = []

    def flush() -> None:
        if not run:
            return
        width = max(len(indent + expr) for indent, expr, _ in run)
        fits = all(
            width + len(COMMENT_GAP) + len(result) <= MAX_LINE_LENGTH
            for _, _, result in run
        )
        for indent, expr, result in run:
            code = indent + expr
            padded = code.ljust(width) if fits else code
            lines.append(f"{padded}{COMMENT_GAP}{result}")
        run.clear()

    for row in rows:
        if isinstance(row, tuple):
            run.append(row)
        else:
            flush()
            lines.append(row)
    flush()
    return lines
