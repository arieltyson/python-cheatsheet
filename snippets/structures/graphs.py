from collections import defaultdict
from collections.abc import Iterator


def build_graph(
    edges: list[tuple[int, int]], directed: bool = False
) -> defaultdict[int, list[int]]:
    """Return an adjacency list from (source, target) pairs."""
    graph = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)
        if not directed:
            graph[target].append(source)
    return graph


def build_weighted_graph(
    edges: list[tuple[int, int, int]],
) -> defaultdict[int, list[tuple[int, int]]]:
    """Return {source: [(target, weight), ...]} for directed edges."""
    graph = defaultdict(list)
    for source, target, weight in edges:
        graph[source].append((target, weight))
    return graph


def grid_neighbors(
    grid: list[list[int]], row: int, col: int
) -> Iterator[tuple[int, int]]:
    """Yield the in-bounds cells up, down, left and right of a cell."""
    rows, cols = len(grid), len(grid[0])
    for row_step, col_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_row, next_col = row + row_step, col + col_step
        if 0 <= next_row < rows and 0 <= next_col < cols:
            yield next_row, next_col


def demo_graphs() -> None:
    graph = build_graph([(0, 1), (1, 2)])
    assert graph[1] == [0, 2]
    # Nodes with no edges read as [] (and get inserted)
    assert graph[9] == []
    weighted = build_weighted_graph([(0, 1, 5), (0, 2, 1)])
    assert weighted[0] == [(1, 5), (2, 1)]
    grid = [[0, 1], [1, 1]]
    assert list(grid_neighbors(grid, 0, 0)) == [(1, 0), (0, 1)]
