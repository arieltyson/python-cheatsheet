"""Turn Python source into highlighted HTML lines at build time."""

import builtins
import html
import io
import keyword
import token
import tokenize

KEYWORDS = frozenset(keyword.kwlist)
BUILTINS = (
    frozenset(
        name for name in dir(builtins) if not name.startswith("_")
    )
    - KEYWORDS
)
STRING_STARTS = {
    getattr(token, name)
    for name in ("FSTRING_START", "TSTRING_START")
    if hasattr(token, name)
}
STRING_ENDS = {
    getattr(token, name)
    for name in ("FSTRING_END", "TSTRING_END")
    if hasattr(token, name)
}
MAX_INDENT_LEVEL = 6

Segment = tuple[str, str | None]


def highlight(source: str) -> str:
    """Return one line span per source line, with tokens wrapped."""
    raw_lines = source.split("\n")
    rendered = _split_lines(_segments(source))
    return "".join(
        f'<span class="line i{_indent_level(raw)}">{body}</span>'
        for raw, body in zip(raw_lines, rendered, strict=True)
    )


def _indent_level(line: str) -> int:
    spaces = len(line) - len(line.lstrip(" "))
    return min(spaces // 4, MAX_INDENT_LEVEL)


def _segments(source: str) -> list[Segment]:
    line_starts = [0]
    for line in source.split("\n"):
        line_starts.append(line_starts[-1] + len(line) + 1)

    def offset(position: tuple[int, int]) -> int:
        row, column = position
        return line_starts[row - 1] + column

    segments: list[Segment] = []
    emitted_up_to = 0
    string_depth = 0
    string_start = 0
    previous_name = ""
    readline = io.StringIO(source).readline
    for tok in tokenize.generate_tokens(readline):
        if tok.type in STRING_STARTS:
            if string_depth == 0:
                string_start = offset(tok.start)
            string_depth += 1
            continue
        if tok.type in STRING_ENDS:
            string_depth -= 1
            if string_depth == 0:
                start, end = string_start, offset(tok.end)
                segments.append((source[emitted_up_to:start], None))
                segments.append((source[start:end], "str"))
                emitted_up_to = end
            continue
        if string_depth:
            continue

        css_class = _classify(tok, previous_name)
        if tok.type == token.NAME:
            previous_name = tok.string
        if css_class is None:
            continue
        start, end = offset(tok.start), offset(tok.end)
        segments.append((source[emitted_up_to:start], None))
        segments.append((source[start:end], css_class))
        emitted_up_to = end

    segments.append((source[emitted_up_to:], None))
    return segments


def _classify(
    tok: tokenize.TokenInfo, previous_name: str
) -> str | None:
    match tok.type:
        case token.STRING:
            return "str"
        case token.NUMBER:
            return "num"
        case token.COMMENT:
            return "com"
        case token.NAME if previous_name in {"def", "class"}:
            return "fn"
        case token.NAME if tok.string in KEYWORDS:
            return "kw"
        case token.NAME if tok.string in BUILTINS:
            return "bi"
    return None


def _split_lines(segments: list[Segment]) -> list[str]:
    lines: list[str] = []
    current: list[str] = []
    for text, css_class in segments:
        for index, part in enumerate(text.split("\n")):
            if index:
                lines.append("".join(current))
                current = []
            if not part:
                continue
            escaped = html.escape(part, quote=False)
            current.append(
                f'<span class="{css_class}">{escaped}</span>'
                if css_class
                else escaped
            )
    lines.append("".join(current))
    return lines
