"""Checks against the built dist/index.html, not the source."""

import tempfile
import unittest
from html.parser import HTMLParser
from itertools import pairwise
from pathlib import Path

from tools.build import MANIFEST, SNIPPETS, build
from tools.manifest import load_site


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.headings: list[int] = []
        self.hidden_in_main: list[str] = []
        self.styled: list[str] = []
        self.unnamed_buttons = 0
        self.html_lang = None
        self._main_depth = 0
        self._button_text = None
        self._button_label = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.html_lang = attributes.get("lang")
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if "style" in attributes:
            self.styled.append(tag)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append(int(tag[1]))
        if tag == "main":
            self._main_depth += 1
        if self._main_depth and "hidden" in attributes:
            self.hidden_in_main.append(tag)
        if tag == "button":
            self._button_text = ""
            self._button_label = attributes.get("aria-label")

    def handle_endtag(self, tag: str) -> None:
        if tag == "main":
            self._main_depth -= 1
        if tag == "button":
            if (
                not (self._button_text or "").strip()
                and not self._button_label
            ):
                self.unnamed_buttons += 1
            self._button_text = None

    def handle_data(self, data: str) -> None:
        if self._button_text is not None:
            self._button_text += data


class BuiltPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.page = build(Path(cls.tempdir.name) / "dist").read_text(
            encoding="utf-8"
        )
        cls.parser = PageParser()
        cls.parser.feed(cls.page)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def test_every_entry_is_on_the_page(self) -> None:
        for entry in load_site(MANIFEST, SNIPPETS).entries():
            with self.subTest(entry=entry.id):
                self.assertIn(entry.id, self.parser.ids)

    def test_ids_are_unique(self) -> None:
        duplicates = {
            i for i in self.parser.ids if self.parser.ids.count(i) > 1
        }
        self.assertEqual(duplicates, set())

    def test_nothing_in_main_is_hidden(self) -> None:
        self.assertEqual(self.parser.hidden_in_main, [])
        self.assertNotIn("display: none", self.page.split("<main")[1])

    def test_no_inline_style_attributes(self) -> None:
        # Inline styles would break the Content-Security-Policy
        self.assertEqual(self.parser.styled, [])

    def test_headings_never_skip_a_level(self) -> None:
        levels = self.parser.headings
        self.assertEqual(levels[0], 1)
        self.assertEqual(levels.count(1), 1)
        for previous, current in pairwise(levels):
            self.assertLessEqual(current, previous + 1)

    def test_buttons_have_names(self) -> None:
        self.assertEqual(self.parser.unnamed_buttons, 0)

    def test_language_is_set(self) -> None:
        self.assertEqual(self.parser.html_lang, "en")


if __name__ == "__main__":
    unittest.main()
