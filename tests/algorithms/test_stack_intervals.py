import random
import unittest
from itertools import pairwise

from snippets.algorithms.intervals import (
    merge_intervals,
    min_meeting_rooms,
)
from snippets.algorithms.monotonic_stack import next_greater

GENERATOR = random.Random(5)


def random_intervals() -> list[list[int]]:
    intervals = []
    for _ in range(GENERATOR.randint(0, 8)):
        start = GENERATOR.randint(0, 10)
        intervals.append([start, start + GENERATOR.randint(1, 5)])
    return intervals


class NextGreaterTests(unittest.TestCase):
    def test_matches_brute_force(self) -> None:
        for _ in range(300):
            values = [
                GENERATOR.randint(0, 5)
                for _ in range(GENERATOR.randint(0, 10))
            ]
            expected = [
                next(
                    (
                        later
                        for later in values[i + 1 :]
                        if later > value
                    ),
                    -1,
                )
                for i, value in enumerate(values)
            ]
            self.assertEqual(next_greater(values), expected)


class IntervalTests(unittest.TestCase):
    def test_merge_examples(self) -> None:
        self.assertEqual(
            merge_intervals([[8, 10], [1, 3], [2, 6], [15, 18]]),
            [[1, 6], [8, 10], [15, 18]],
        )
        self.assertEqual(merge_intervals([[1, 4], [4, 5]]), [[1, 5]])
        self.assertEqual(merge_intervals([]), [])

    def test_merge_covers_the_same_points(self) -> None:
        for _ in range(300):
            intervals = random_intervals()
            merged = merge_intervals(intervals)
            covered = {
                point * 2
                for start, end in intervals
                for point in range(start, end + 1)
            }
            merged_points = {
                point * 2
                for start, end in merged
                for point in range(start, end + 1)
            }
            self.assertEqual(merged_points, covered)
            for previous, current in pairwise(merged):
                self.assertLess(previous[1], current[0])

    def test_meeting_rooms_matches_brute_force(self) -> None:
        for _ in range(300):
            intervals = random_intervals()
            busiest = max(
                (
                    sum(
                        start <= moment < end
                        for start, end in intervals
                    )
                    for moment in range(0, 16)
                ),
                default=0,
            )
            self.assertEqual(min_meeting_rooms(intervals), busiest)


if __name__ == "__main__":
    unittest.main()
