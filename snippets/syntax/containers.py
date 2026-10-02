import math


def demo_list_operations() -> None:
    items = [3, 1]
    items.append(4)
    items.extend([5, 9])
    assert items == [3, 1, 4, 5, 9]
    assert items.pop() == 9
    assert items.pop(0) == 3
    items.insert(0, 2)
    items.remove(4)
    assert items == [2, 1, 5]
    assert items.index(5) == 2
    assert items[-1] == 5
    assert items.count(1) == 1
    items.reverse()
    assert items == [5, 1, 2]
    del items[0]
    assert items == [1, 2]


def demo_comprehensions() -> None:
    assert [n * n for n in range(4)] == [0, 1, 4, 9]
    assert [n for n in range(7) if n % 3 == 0] == [0, 3, 6]
    labels = ["even" if n % 2 == 0 else "odd" for n in range(3)]
    assert labels == ["even", "odd", "even"]
    assert {char: i for i, char in enumerate("ab")} == {"a": 0, "b": 1}
    assert {len(word) for word in ["hi", "yo", "hey"]} == {2, 3}
    nested = [[1, 2], [3]]
    assert [value for row in nested for value in row] == [1, 2, 3]


def demo_grid() -> None:
    rows, cols = 2, 3
    grid = [[0] * cols for _ in range(rows)]
    grid[0][1] = 7
    assert grid == [[0, 7, 0], [0, 0, 0]]
    # Bug: * repeats the same inner list, so every row changes
    shared = [[0] * cols] * rows
    shared[0][1] = 7
    assert shared == [[0, 7, 0], [0, 7, 0]]
    transposed = [list(column) for column in zip(*grid, strict=True)]
    assert transposed == [[0, 0], [7, 0], [0, 0]]
    assert (len(grid), len(grid[0])) == (rows, cols)


def demo_unpacking() -> None:
    first, *rest = [1, 2, 3]
    assert (first, rest) == (1, [2, 3])
    *init, last = [1, 2, 3]
    assert (init, last) == ([1, 2], 3)
    left, right = 1, 2
    left, right = right, left
    assert (left, right) == (2, 1)
    (row, col), label = (2, 3), "goal"
    assert (row, col, label) == (2, 3, "goal")


def demo_copying() -> None:
    original = [[1], [2]]
    shallow = original.copy()
    shallow[0].append(9)
    # A shallow copy shares the inner lists
    assert original == [[1, 9], [2]]
    # Copying each row makes the copies independent
    deep = [row[:] for row in original]
    deep[0].append(5)
    assert deep == [[1, 9, 5], [2]]
    assert original == [[1, 9], [2]]


def demo_dict_operations() -> None:
    ages = {"ada": 36}
    ages["bo"] = 25
    assert ages.get("cy") is None
    assert ages.get("cy", 0) == 0
    assert "ada" in ages
    ages.setdefault("cy", 0)
    ages["cy"] += 1
    assert ages.pop("bo") == 25
    # Dicts keep insertion order
    assert list(ages) == ["ada", "cy"]
    assert list(ages.items()) == [("ada", 36), ("cy", 1)]
    del ages["cy"]
    assert ages | {"dee": 40} == {"ada": 36, "dee": 40}


def demo_sort_dict() -> None:
    counts = {"b": 2, "a": 3, "c": 1}
    by_count = sorted(counts.items(), key=lambda item: -item[1])
    assert by_count == [("a", 3), ("b", 2), ("c", 1)]
    assert sorted(counts) == ["a", "b", "c"]
    assert max(counts, key=counts.get) == "a"
    assert dict(sorted(counts.items())) == {"a": 3, "b": 2, "c": 1}


def demo_set_operations() -> None:
    first, second = {1, 2, 3}, {2, 3, 4}
    assert first | second == {1, 2, 3, 4}
    assert first & second == {2, 3}
    assert first - second == {1}
    assert first ^ second == {1, 4}
    assert {1, 2} <= first
    seen = set()
    seen.add(5)
    seen.discard(9)
    assert 5 in seen
    # Remove duplicates but keep the original order
    assert list(dict.fromkeys([3, 1, 3, 2])) == [3, 1, 2]


def demo_hashable_keys() -> None:
    visited = {(0, 0), (0, 1)}
    assert (0, 1) in visited
    # Lists are not hashable: convert to a tuple to use as a key
    groups = {tuple(sorted("eat")): ["eat"]}
    assert ("a", "e", "t") in groups
    assert frozenset({1, 2}) in {frozenset({2, 1})}


def demo_infinity() -> None:
    best = math.inf
    assert best == float("inf")
    assert min(best, 5) == 5
    assert -math.inf < -(10**18)
    # Python ints never overflow
    assert 2**100 == 1267650600228229401496703205376
