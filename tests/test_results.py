import unittest

from tools.results import asserts_as_results


class AssertsAsResultsTests(unittest.TestCase):
    def test_equality_becomes_result_comment(self) -> None:
        self.assertEqual(
            asserts_as_results("assert sum([1, 2]) == 3"),
            "sum([1, 2])  # 3",
        )

    def test_aligns_consecutive_results(self) -> None:
        self.assertEqual(
            asserts_as_results(
                "assert len(text) == 5\nassert text.upper() == 'HELLO'"
            ).split("\n"),
            ["len(text)     # 5", "text.upper()  # 'HELLO'"],
        )

    def test_membership_and_negation(self) -> None:
        self.assertEqual(
            asserts_as_results("assert 'a' in word\nassert not word"),
            "'a' in word  # True\nword         # False",
        )

    def test_is_none(self) -> None:
        self.assertEqual(
            asserts_as_results("assert lookup.get(9) is None"),
            "lookup.get(9)  # None",
        )

    def test_keeps_indentation_and_other_lines(self) -> None:
        source = "for n in range(2):\n    assert n < 2\ntotal = 0"
        self.assertEqual(
            asserts_as_results(source),
            "for n in range(2):\n    n < 2  # True\ntotal = 0",
        )

    def test_leaves_multiline_and_messaged_asserts(self) -> None:
        source = 'assert (\n    x == 1\n)\nassert y == 2, "why"'
        self.assertEqual(asserts_as_results(source), source)

    def test_skips_alignment_when_it_would_overflow(self) -> None:
        long_name = "a" * 68
        source = f"assert {long_name} == 1\nassert b == 2"
        self.assertEqual(
            asserts_as_results(source),
            f"{long_name}  # 1\nb  # 2",
        )


if __name__ == "__main__":
    unittest.main()
