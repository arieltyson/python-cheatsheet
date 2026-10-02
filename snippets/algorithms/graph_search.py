from collections import deque
from collections.abc import Iterator


def bfs_order(graph: dict[int, list[int]], start: int) -> list[int]:
    """Return nodes reachable from start, nearest first."""
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def grid_neighbors(
    grid: list[list], row: int, col: int
) -> Iterator[tuple[int, int]]:
    """Yield the in-bounds cells up, down, left and right of a cell."""
    rows, cols = len(grid), len(grid[0])
    for row_step, col_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_row, next_col = row + row_step, col + col_step
        if 0 <= next_row < rows and 0 <= next_col < cols:
            yield next_row, next_col


def shortest_path_grid(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> int:
    """Return the fewest steps from start to goal on 0 cells, or -1."""
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        cell, steps = queue.popleft()
        if cell == goal:
            return steps
        for row, col in grid_neighbors(grid, *cell):
            if grid[row][col] == 0 and (row, col) not in visited:
                visited.add((row, col))
                queue.append(((row, col), steps + 1))
    return -1


def dfs_recursive(graph: dict[int, list[int]], start: int) -> list[int]:
    """Return nodes reachable from start in depth-first order."""
    visited = set()
    order = []

    def visit(node: int) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def dfs_iterative(graph: dict[int, list[int]], start: int) -> list[int]:
    """Return the dfs_recursive order using an explicit stack."""
    visited = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Reversed so the first neighbour is popped (visited) first
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def count_islands(grid: list[list[str]]) -> int:
    """Return the number of 4-connected groups of "1" cells."""
    seen = set()
    islands = 0
    for row, line in enumerate(grid):
        for col, value in enumerate(line):
            if value != "1" or (row, col) in seen:
                continue
            islands += 1
            seen.add((row, col))
            stack = [(row, col)]
            while stack:
                for cell in grid_neighbors(grid, *stack.pop()):
                    next_row, next_col = cell
                    is_land = grid[next_row][next_col] == "1"
                    if is_land and cell not in seen:
                        seen.add(cell)
                        stack.append(cell)
    return islands
