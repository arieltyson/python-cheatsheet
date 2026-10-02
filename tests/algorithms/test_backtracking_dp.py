import itertools
import random
import unittest

from snippets.algorithms.backtracking import (
    combinations,
    permutations,
    subsets,
)
from snippets.algorithms.dynamic_programming import (
    climb_stairs,
    climb_stairs_memo,
    coin_change,
    house_robber,
    knapsack,
    longest_common_subsequence,
    longest_increasing_subsequence,
    unique_grid_paths,
)

GENERATOR = random.Random(13)


def as_sets(lists: list[list[int]]) -> list[tuple[int, ...]]:
    return sorted(tuple(item) for item in lists)


class BacktrackingTests(unittest.TestCase):
    def test_subsets(self) -> None:
        values = [1, 2, 3]
        expected = [
            combo
            for size in range(len(values) + 1)
            for combo in itertools.combinations(values, size)
        ]
        self.assertEqual(as_sets(subsets(values)), sorted(expected))
        self.assertEqual(subsets([]), [[]])

    def test_combinations(self) -> None:
        values = [1, 2, 3, 4]
        for size in range(5):
            self.assertEqual(
                as_sets(combinations(values, size)),
                sorted(itertools.combinations(values, size)),
            )

    def test_permutations(self) -> None:
        self.assertEqual(
            as_sets(permutations([1, 2, 3])),
            sorted(itertools.permutations([1, 2, 3])),
        )
        self.assertEqual(permutations([]), [[]])


class DynamicProgrammingTests(unittest.TestCase):
    def test_climb_stairs(self) -> None:
        expected = [1, 1, 2, 3, 5, 8, 13]
        for steps, ways in enumerate(expected):
            self.assertEqual(climb_stairs(steps), ways)
            self.assertEqual(climb_stairs_memo(steps), ways)

    def test_house_robber_matches_brute_force(self) -> None:
        for _ in range(200):
            values = [
                GENERATOR.randint(0, 9)
                for _ in range(GENERATOR.randint(0, 8))
            ]
            best = 0
            for mask in range(1 << len(values)):
                if mask & (mask >> 1):
                    continue
                total = sum(
                    v for i, v in enumerate(values) if mask >> i & 1
                )
                best = max(best, total)
            self.assertEqual(house_robber(values), best)

    def test_coin_change(self) -> None:
        self.assertEqual(coin_change([1, 2, 5], 11), 3)
        self.assertEqual(coin_change([2], 3), -1)
        self.assertEqual(coin_change([1], 0), 0)
        self.assertEqual(coin_change([3, 7], 12), 4)

    def test_knapsack_matches_brute_force(self) -> None:
        for _ in range(200):
            count = GENERATOR.randint(0, 6)
            weights = [GENERATOR.randint(1, 6) for _ in range(count)]
            values = [GENERATOR.randint(0, 9) for _ in range(count)]
            capacity = GENERATOR.randint(0, 12)
            best = max(
                sum(values[i] for i in chosen)
                for size in range(count + 1)
                for chosen in itertools.combinations(range(count), size)
                if sum(weights[i] for i in chosen) <= capacity
            )
            self.assertEqual(knapsack(weights, values, capacity), best)

    def test_unique_grid_paths(self) -> None:
        self.assertEqual(unique_grid_paths(3, 7), 28)
        self.assertEqual(unique_grid_paths(1, 1), 1)
        self.assertEqual(unique_grid_paths(3, 2), 3)

    def test_lcs(self) -> None:
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)
        self.assertEqual(longest_common_subsequence("abc", "def"), 0)
        self.assertEqual(longest_common_subsequence("", "abc"), 0)

    def test_lis_matches_quadratic_dp(self) -> None:
        for _ in range(300):
            values = [
                GENERATOR.randint(0, 6)
                for _ in range(GENERATOR.randint(0, 10))
            ]
            lengths = [1] * len(values)
            for i in range(len(values)):
                for j in range(i):
                    if values[j] < values[i]:
                        lengths[i] = max(lengths[i], lengths[j] + 1)
            self.assertEqual(
                longest_increasing_subsequence(values),
                max(lengths, default=0),
            )


if __name__ == "__main__":
    unittest.main()
