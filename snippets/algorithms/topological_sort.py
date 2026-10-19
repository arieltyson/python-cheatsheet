from collections import defaultdict, deque


def topological_order(
    count: int, edges: list[tuple[int, int]]
) -> list[int] | None:
    """Return nodes 0..count-1 so every edge (a, b) has a before b.

    Return None if the edges contain a cycle.
    """
    graph = defaultdict(list)
    in_degree = [0] * count
    for before, after in edges:
        graph[before].append(after)
        in_degree[after] += 1
    queue = deque(node for node in range(count) if in_degree[node] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == count else None


def has_cycle(graph: dict[int, list[int]]) -> bool:
    """Directed graph: DFS with a set for the current path."""
    visiting, done = set(), set()

    def visit(node: int) -> bool:
        if node in visiting:  # back edge to the current path
            return True
        if node in done:
            return False
        visiting.add(node)
        if any(visit(neighbor) for neighbor in graph.get(node, [])):
            return True
        visiting.remove(node)
        done.add(node)
        return False

    return any(visit(node) for node in graph)
