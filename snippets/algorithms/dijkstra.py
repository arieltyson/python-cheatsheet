import heapq
import math


def dijkstra(
    graph: dict[int, list[tuple[int, int]]], source: int
) -> dict[int, int]:
    """Return the shortest distance from source to each reachable node.

    graph maps node -> [(neighbor, weight), ...]; weights must be >= 0.
    """
    distances = {source: 0}
    heap = [(0, source)]
    while heap:
        distance, node = heapq.heappop(heap)
        # Skip stale entries left behind by a later, shorter path
        if distance > distances[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            candidate = distance + weight
            if candidate < distances.get(neighbor, math.inf):
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distances
