import math
import random
import unittest

from snippets.algorithms.dijkstra import dijkstra


def bellman_ford(
    count: int, edges: list[tuple[int, int, int]], source: int
):
    distances = [math.inf] * count
    distances[source] = 0
    for _ in range(count - 1):
        for start, end, weight in edges:
            distances[end] = min(
                distances[end], distances[start] + weight
            )
    return {node: d for node, d in enumerate(distances) if d < math.inf}


class DijkstraTests(unittest.TestCase):
    def test_example(self) -> None:
        graph = {0: [(1, 4), (2, 1)], 2: [(1, 2), (3, 5)], 1: [(3, 1)]}
        self.assertEqual(dijkstra(graph, 0), {0: 0, 1: 3, 2: 1, 3: 4})

    def test_single_node(self) -> None:
        self.assertEqual(dijkstra({}, 5), {5: 0})

    def test_matches_bellman_ford(self) -> None:
        generator = random.Random(21)
        for _ in range(300):
            count = generator.randint(1, 8)
            edges = [
                (
                    generator.randrange(count),
                    generator.randrange(count),
                    generator.randint(0, 9),
                )
                for _ in range(generator.randint(0, 20))
            ]
            graph = {}
            for start, end, weight in edges:
                graph.setdefault(start, []).append((end, weight))
            self.assertEqual(
                dijkstra(graph, 0), bellman_ford(count, edges, 0)
            )


if __name__ == "__main__":
    unittest.main()
