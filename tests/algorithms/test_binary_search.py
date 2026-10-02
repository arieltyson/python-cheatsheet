import bisect
import random
import unittest

from snippets.algorithms.binary_search import (
    binary_search,
    first_true,
    lower_bound,
    min_eating_speed,
    upper_bound,
)


def random_sorted_lists(count: int = 300) -> list[list[int]]:
    generator = random.Random(7)
    return [
        sorted(
            generator.randint(-5, 5)
            for _ in range(generator.randint(0, 12))
        )
        for _ in range(count)
    ]


class BinarySearchTests(unittest.TestCase):
    def test_finds_present_and_rejects_absent(self) -> None:
        for values in random_sorted_lists():
            for target in range(-6, 7):
                index = binary_search(values, target)
                if target in values:
                    self.assertEqual(values[index], target)
                else:
                    self.assertEqual(index, -1)

    def test_bounds_match_bisect(self) -> None:
        for values in random_sorted_lists():
            for target in range(-6, 7):
                self.assertEqual(
                    lower_bound(values, target),
                    bisect.bisect_left(values, target),
                )
                self.assertEqual(
                    upper_bound(values, target),
                    bisect.bisect_right(values, target),
                )

    def test_first_true(self) -> None:
        self.assertEqual(first_true(0, 100, lambda x: x * x >= 50), 8)
        self.assertEqual(first_true(5, 5, lambda x: True), 5)
        self.assertEqual(first_true(1, 10, lambda x: True), 1)

    def test_min_eating_speed(self) -> None:
        self.assertEqual(min_eating_speed([3, 6, 7, 11], 8), 4)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 5), 30)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 6), 23)
        self.assertEqual(min_eating_speed([1], 1), 1)


if __name__ == "__main__":
    unittest.main()
