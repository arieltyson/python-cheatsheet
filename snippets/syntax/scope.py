def demo_nonlocal() -> None:
    tree = {1: [2, 3], 2: [4], 3: [], 4: []}
    visited = 0
    deepest = 0
    order = []

    def dfs(node: int, depth: int) -> None:
        # Reassigning an outer variable needs nonlocal
        nonlocal visited, deepest
        visited += 1
        deepest = max(deepest, depth)
        # Mutating an outer list or dict does not
        order.append(node)
        for child in tree[node]:
            dfs(child, depth + 1)

    dfs(1, 1)
    assert visited == 4
    assert deepest == 3
    assert order == [1, 2, 4, 3]
