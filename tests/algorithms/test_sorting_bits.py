import random
import unittest

from snippets.algorithms.bits import single_number
from snippets.algorithms.sorting import (
    kth_largest,
    merge_sort,
    top_k_largest,
)

GENERATOR = random.Random(17)


def random_lists(count: int = 300) -> list[list[int]]:
    return [
        [
            GENERATOR.randint(-5, 5)
            for _ in range(GENERATOR.randint(0, 15))
        ]
        for _ in range(count)
    ]


class SortingTests(unittest.TestCase):
    def test_merge_sort(self) -> None:
        for values in random_lists():
            original = values[:]
            self.assertEqual(merge_sort(values), sorted(values))
            self.assertEqual(values, original)

    def test_kth_largest(self) -> None:
        for values in random_lists():
            ranked = sorted(values, reverse=True)
            for k in range(1, len(values) + 1):
                self.assertEqual(kth_largest(values, k), ranked[k - 1])

    def test_top_k(self) -> None:
        for values in random_lists():
            for k in range(len(values) + 2):
                self.assertEqual(
                    top_k_largest(values, k),
                    sorted(values, reverse=True)[:k],
                )


class BitTests(unittest.TestCase):
    def test_single_number(self) -> None:
        self.assertEqual(single_number([4, 1, 2, 1, 2]), 4)
        self.assertEqual(single_number([-3]), -3)


if __name__ == "__main__":
    unittest.main()
