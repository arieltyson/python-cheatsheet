import random
import unittest

from snippets.algorithms.spreadsheet import (
    CachedSpreadsheet,
    Spreadsheet,
    parse_expression,
)
from snippets.algorithms.topological_sort import has_cycle

GENERATOR = random.Random(29)
KEYS = ["A1", "B1", "C1", "D1", "E1", "F1"]


def random_expression() -> str:
    if GENERATOR.random() < 0.3:
        return str(GENERATOR.randint(-9, 9))
    terms = GENERATOR.choices(
        [*KEYS, "1", "7"], k=GENERATOR.randint(1, 3)
    )
    return "=" + " + ".join(terms)


def read(sheet: Spreadsheet | CachedSpreadsheet, key: str) -> int | str:
    try:
        return sheet.get_cell(key)
    except ValueError as e:
        return str(e)


class ParseTests(unittest.TestCase):
    def test_parse(self) -> None:
        self.assertEqual(parse_expression("-10"), (-10, []))
        self.assertEqual(
            parse_expression("=A1 + 5+B2+2"), (7, ["A1", "B2"])
        )
        self.assertEqual(parse_expression("=A1+A1"), (0, ["A1", "A1"]))


class SpreadsheetTests(unittest.TestCase):
    def test_worked_example(self) -> None:
        for sheet in (Spreadsheet(), CachedSpreadsheet()):
            with self.subTest(sheet=type(sheet).__name__):
                sheet.set_cell("A1", "10")
                sheet.set_cell("B1", "=A1+5")
                sheet.set_cell("C1", "=A1+B1+2")
                self.assertEqual(sheet.get_cell("C1"), 27)
                sheet.set_cell("A1", "20")
                self.assertEqual(sheet.get_cell("B1"), 25)
                self.assertEqual(sheet.get_cell("C1"), 47)

    def test_cycle_found_on_read(self) -> None:
        sheet = Spreadsheet()
        sheet.set_cell("A1", "=C1+10")
        sheet.set_cell("B1", "=A1+5")
        sheet.set_cell("C1", "=D1+B1+2")
        sheet.set_cell("D1", "34")
        with self.assertRaisesRegex(ValueError, "^Cycle detected$"):
            sheet.get_cell("C1")
        self.assertEqual(sheet.get_cell("D1"), 34)
        sheet.set_cell("Z1", "=Z1+5")
        self.assertEqual(read(sheet, "Z1"), "Cycle detected")

    def test_cycle_rejected_on_write(self) -> None:
        sheet = CachedSpreadsheet()
        sheet.set_cell("A1", "=B1")
        with self.assertRaisesRegex(ValueError, "^Cycle detected$"):
            sheet.set_cell("B1", "=A1+1")
        with self.assertRaisesRegex(ValueError, "^Cycle detected$"):
            sheet.set_cell("C1", "=C1")
        self.assertEqual(sheet.get_cell("A1"), 0)

    def test_overwrite_drops_old_edges(self) -> None:
        sheet = CachedSpreadsheet()
        sheet.set_cell("B1", "=A1")
        sheet.set_cell("B1", "=C1")
        self.assertEqual(sheet.dependents["A1"], set())
        sheet.set_cell("A1", "=B1")  # no cycle: B1 no longer reads A1
        self.assertEqual(sheet.get_cell("A1"), 0)

    def test_diamond_is_not_a_cycle(self) -> None:
        sheet = Spreadsheet()
        sheet.set_cell("A1", "1")
        previous = "A1"
        for row in range(2, 60):
            sheet.set_cell(f"A{row}", f"={previous}+{previous}")
            previous = f"A{row}"
        self.assertEqual(sheet.get_cell(previous), 2**58)

    def test_cached_matches_uncached(self) -> None:
        for _ in range(300):
            plain, cached = Spreadsheet(), CachedSpreadsheet()
            for _ in range(20):
                key = GENERATOR.choice(KEYS)
                expression = random_expression()
                plain.set_cell(key, expression)
                if read(plain, key) == "Cycle detected":
                    with self.assertRaises(ValueError):
                        cached.set_cell(key, expression)
                    del plain.cells[key]
                    if key in cached.cells:
                        plain.cells[key] = cached.cells[key]
                else:
                    cached.set_cell(key, expression)
                for check in KEYS:
                    self.assertEqual(
                        read(cached, check), read(plain, check)
                    )


class CycleCheckTests(unittest.TestCase):
    def test_has_cycle(self) -> None:
        self.assertFalse(has_cycle({0: [1, 2], 1: [3], 2: [3]}))
        self.assertTrue(has_cycle({0: [1], 1: [2], 2: [0]}))
        self.assertTrue(has_cycle({0: [0]}))
        self.assertFalse(has_cycle({}))


if __name__ == "__main__":
    unittest.main()
