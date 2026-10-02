import html
import re
import unittest

from tools.highlight import highlight

TAG = re.compile(r"<[^>]+>")


def plain_lines(rendered: str) -> list[str]:
    lines = re.findall(
        r'<span class="line i\d">(.*?)</span>(?=<span class="line|$)',
        rendered,
    )
    return [html.unescape(TAG.sub("", line)) for line in lines]


class HighlightTests(unittest.TestCase):
    def assert_round_trips(self, source: str) -> None:
        self.assertEqual(
            plain_lines(highlight(source)), source.split("\n")
        )

    def test_round_trips_source_exactly(self) -> None:
        self.assert_round_trips(
            "def total(values: list[int]) -> int:\n"
            "    # Sum <values> & return\n"
            "    return sum(values) if values else 0"
        )

    def test_round_trips_multiline_strings(self) -> None:
        self.assert_round_trips('text = """a\nb < c\n"""\nprint(text)')

    def test_round_trips_nested_f_strings(self) -> None:
        self.assert_round_trips(
            'label = f"{name!r:>{width}} {f"{cost:,.2f}"} {{x}}"'
        )

    def test_classifies_tokens(self) -> None:
        rendered = highlight(
            "def area(side):\n    return abs(side) * 2  # ok"
        )
        self.assertIn('<span class="kw">def</span>', rendered)
        self.assertIn('<span class="fn">area</span>', rendered)
        self.assertIn('<span class="kw">return</span>', rendered)
        self.assertIn('<span class="bi">abs</span>', rendered)
        self.assertIn('<span class="num">2</span>', rendered)
        self.assertIn('<span class="com"># ok</span>', rendered)

    def test_f_string_is_one_string_span(self) -> None:
        rendered = highlight('f"${amount:,.2f}"')
        self.assertIn(
            '<span class="str">f"${amount:,.2f}"</span>', rendered
        )

    def test_escapes_html(self) -> None:
        rendered = highlight('tag = "<script>"')
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_marks_indent_levels(self) -> None:
        rendered = highlight("if x:\n    if y:\n        pass")
        self.assertIn('class="line i0"', rendered)
        self.assertIn('class="line i1"', rendered)
        self.assertIn('class="line i2"', rendered)


if __name__ == "__main__":
    unittest.main()
