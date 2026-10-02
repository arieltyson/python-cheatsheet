import random
import unittest

from snippets.algorithms.prefix_sums import (
    count_subarrays_with_sum,
    prefix_sums,
)
from snippets.algorithms.sliding_window import (
    longest_unique_substring,
    longest_with_k_distinct,
    max_window_sum,
)
from snippets.algorithms.two_pointers import (
    is_palindrome,
    pair_with_sum,
    remove_duplicates,
    three_sum,
)

GENERATOR = random.Random(11)


def random_lists(count: int = 200, size: int = 10) -> list[list[int]]:
    return [
        [
            GENERATOR.randint(-4, 4)
            for _ in range(GENERATOR.randint(0, size))
        ]
        for _ in range(count)
    ]


def random_texts(count: int = 200) -> list[str]:
    return [
        "".join(
            GENERATOR.choice("abcd")
            for _ in range(GENERATOR.randint(0, 12))
        )
        for _ in range(count)
    ]


class TwoPointerTests(unittest.TestCase):
    def test_pair_with_sum(self) -> None:
        self.assertEqual(pair_with_sum([1, 2, 4, 7, 11], 9), (1, 3))
        self.assertIsNone(pair_with_sum([1, 2], 9))
        self.assertIsNone(pair_with_sum([], 0))
        self.assertIsNone(pair_with_sum([5], 10))

    def test_three_sum_matches_brute_force(self) -> None:
        for values in random_lists(size=8):
            expected = sorted(
                {
                    tuple(sorted((values[i], values[j], values[k])))
                    for i in range(len(values))
                    for j in range(i + 1, len(values))
                    for k in range(j + 1, len(values))
                    if values[i] + values[j] + values[k] == 0
                }
            )
            actual = sorted(
                tuple(triplet) for triplet in three_sum(values)
            )
            self.assertEqual(actual, expected)

    def test_remove_duplicates(self) -> None:
        for values in random_lists():
            values.sort()
            expected = sorted(set(values))
            length = remove_duplicates(values)
            self.assertEqual(values[:length], expected)

    def test_is_palindrome(self) -> None:
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome(".,"))
        self.assertFalse(is_palindrome("race a car"))


class SlidingWindowTests(unittest.TestCase):
    def test_max_window_sum(self) -> None:
        for values in random_lists():
            for size in range(1, len(values) + 1):
                expected = max(
                    sum(values[i : i + size])
                    for i in range(len(values) - size + 1)
                )
                self.assertEqual(max_window_sum(values, size), expected)

    def test_k_distinct_matches_brute_force(self) -> None:
        for text in random_texts():
            for k in range(4):
                expected = max(
                    (
                        end - start
                        for start in range(len(text))
                        for end in range(start + 1, len(text) + 1)
                        if len(set(text[start:end])) <= k
                    ),
                    default=0,
                )
                self.assertEqual(
                    longest_with_k_distinct(text, k), expected
                )

    def test_unique_substring_matches_brute_force(self) -> None:
        for text in random_texts():
            expected = max(
                (
                    end - start
                    for start in range(len(text))
                    for end in range(start + 1, len(text) + 1)
                    if len(set(text[start:end])) == end - start
                ),
                default=0,
            )
            self.assertEqual(longest_unique_substring(text), expected)
        self.assertEqual(longest_unique_substring("abcabcbb"), 3)


class PrefixSumTests(unittest.TestCase):
    def test_prefix_sums(self) -> None:
        self.assertEqual(prefix_sums([]), [0])
        self.assertEqual(prefix_sums([2, -1, 3]), [0, 2, 1, 4])

    def test_subarray_count_matches_brute_force(self) -> None:
        for values in random_lists():
            for target in range(-3, 4):
                expected = sum(
                    1
                    for start in range(len(values))
                    for end in range(start + 1, len(values) + 1)
                    if sum(values[start:end]) == target
                )
                self.assertEqual(
                    count_subarrays_with_sum(values, target), expected
                )


if __name__ == "__main__":
    unittest.main()
