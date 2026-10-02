import unittest

from snippets.structures.graphs import (
    build_graph,
    build_weighted_graph,
    grid_neighbors,
)


class GraphTests(unittest.TestCase):
    def test_undirected(self) -> None:
        graph = build_graph([(0, 1), (0, 2)])
        self.assertEqual(graph, {0: [1, 2], 1: [0], 2: [0]})

    def test_directed(self) -> None:
        graph = build_graph([(0, 1), (1, 2)], directed=True)
        self.assertEqual(graph, {0: [1], 1: [2]})

    def test_empty(self) -> None:
        self.assertEqual(build_graph([]), {})

    def test_weighted(self) -> None:
        graph = build_weighted_graph([(0, 1, 4), (1, 0, 2)])
        self.assertEqual(graph, {0: [(1, 4)], 1: [(0, 2)]})

    def test_grid_neighbors(self) -> None:
        grid = [[0] * 3 for _ in range(3)]
        self.assertEqual(len(list(grid_neighbors(grid, 1, 1))), 4)
        self.assertEqual(
            sorted(grid_neighbors(grid, 2, 2)), [(1, 2), (2, 1)]
        )
        self.assertEqual(list(grid_neighbors([[0]], 0, 0)), [])


if __name__ == "__main__":
    unittest.main()
