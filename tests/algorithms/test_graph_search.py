import random
import unittest

from snippets.algorithms.graph_search import (
    bfs_order,
    count_islands,
    dfs_iterative,
    dfs_recursive,
    shortest_path_grid,
)
from snippets.algorithms.topological_sort import topological_order

#   0 - 1 - 3
#   |   |
#   2   4 - 5
GRAPH = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1, 5], 5: [4]}


class TraversalTests(unittest.TestCase):
    def test_bfs_visits_by_distance(self) -> None:
        self.assertEqual(bfs_order(GRAPH, 0), [0, 1, 2, 3, 4, 5])
        self.assertEqual(bfs_order({}, 7), [7])

    def test_dfs_orders_agree(self) -> None:
        self.assertEqual(dfs_recursive(GRAPH, 0), [0, 1, 3, 4, 5, 2])
        self.assertEqual(dfs_iterative(GRAPH, 0), [0, 1, 3, 4, 5, 2])
        generator = random.Random(3)
        for _ in range(200):
            graph = {
                node: generator.sample(
                    range(8), generator.randint(0, 3)
                )
                for node in range(8)
            }
            self.assertEqual(
                dfs_iterative(graph, 0), dfs_recursive(graph, 0)
            )


class GridTests(unittest.TestCase):
    def test_shortest_path(self) -> None:
        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]
        self.assertEqual(shortest_path_grid(grid, (0, 0), (2, 0)), 6)
        self.assertEqual(shortest_path_grid(grid, (0, 0), (0, 0)), 0)
        grid[1][2] = 1
        self.assertEqual(shortest_path_grid(grid, (0, 0), (2, 0)), -1)

    def test_count_islands(self) -> None:
        grid = [
            list("11000"),
            list("11000"),
            list("00100"),
            list("00011"),
        ]
        self.assertEqual(count_islands(grid), 3)
        self.assertEqual(count_islands([list("0")]), 0)
        self.assertEqual(count_islands([list("1")]), 1)

    def test_large_island_does_not_recurse(self) -> None:
        grid = [["1"] * 300 for _ in range(300)]
        self.assertEqual(count_islands(grid), 1)


class TopologicalOrderTests(unittest.TestCase):
    def test_respects_every_edge(self) -> None:
        generator = random.Random(9)
        for _ in range(200):
            count = generator.randint(1, 8)
            ranking = generator.sample(range(count), count)
            edges = [
                (first, second)
                for first in range(count)
                for second in range(count)
                if ranking[first] < ranking[second]
                and generator.random() < 0.3
            ]
            order = topological_order(count, edges)
            position = {node: index for index, node in enumerate(order)}
            self.assertEqual(sorted(order), list(range(count)))
            for before, after in edges:
                self.assertLess(position[before], position[after])

    def test_cycle_returns_none(self) -> None:
        self.assertIsNone(
            topological_order(3, [(0, 1), (1, 2), (2, 0)])
        )
        self.assertIsNone(topological_order(1, [(0, 0)]))

    def test_no_edges(self) -> None:
        self.assertEqual(topological_order(3, []), [0, 1, 2])
        self.assertEqual(topological_order(0, []), [])


if __name__ == "__main__":
    unittest.main()
