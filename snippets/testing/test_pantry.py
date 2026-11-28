import unittest


class PantryError(ValueError):
    """Raised for a count below one."""


class Pantry:
    """A small class to test. In a real project it lives in its own
    module, and the test file imports it: from pantry import Pantry."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    @property
    def names(self) -> list[str]:
        return sorted(self._counts)

    def count(self, name: str) -> int:
        return self._counts.get(name, 0)

    def add(self, name: str, count: int) -> None:
        if count <= 0:
            raise PantryError(f"count must be positive, got {count}")
        self._counts[name] = self.count(name) + count


class PantryTests(unittest.TestCase):
    """unittest makes a NEW instance of this class for every test
    method, and setUp runs before each one, so tests never share
    state. Every method whose name starts with test_ is a test."""

    def setUp(self) -> None:
        self.pantry = Pantry()

    def test_starts_empty(self) -> None:
        self.assertEqual(self.pantry.names, [])
        self.assertEqual(self.pantry.count("rice"), 0)

    def test_adding_the_same_item_adds_up(self) -> None:
        self.pantry.add("rice", 2)
        self.pantry.add("rice", 3)
        self.assertEqual(self.pantry.count("rice"), 5)

    def test_names_come_back_a_to_z(self) -> None:
        self.pantry.add("tea", 1)
        self.pantry.add("oats", 1)
        self.assertEqual(self.pantry.names, ["oats", "tea"])

    def test_rejects_counts_below_one(self) -> None:
        # subTest runs the body once per value and reports each one
        for count in (0, -1, -50):
            with self.subTest(count=count):
                with self.assertRaises(PantryError):
                    self.pantry.add("rice", count)
                # nothing was stored
                self.assertEqual(self.pantry.names, [])

    def test_error_message(self) -> None:
        with self.assertRaises(PantryError) as caught:
            self.pantry.add("rice", 0)
        self.assertIn("got 0", str(caught.exception))
