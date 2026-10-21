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


def demo_walrus() -> None:
    # := assigns and returns the value in one expression
    prices = {"apple": 3}
    if (price := prices.get("apple")) is not None:
        prices["apple"] = price + 1
    assert prices == {"apple": 4}
    # Compute once, then both filter and keep the result
    values = [3, 8, 5]
    doubled = [d for v in values if (d := v * 2) > 7]
    assert doubled == [16, 10]
    # Read until a sentinel
    stream = iter([1, 2, 0, 9])
    taken = []
    while (item := next(stream)) != 0:
        taken.append(item)
    assert taken == [1, 2]
