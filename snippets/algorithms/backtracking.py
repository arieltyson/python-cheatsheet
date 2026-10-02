def subsets(values: list[int]) -> list[list[int]]:
    """Return every subset of values."""
    result, path = [], []

    def explore(start: int) -> None:
        result.append(path[:])
        for i in range(start, len(values)):
            path.append(values[i])
            explore(i + 1)
            path.pop()

    explore(0)
    return result


def combinations(values: list[int], size: int) -> list[list[int]]:
    """Return every way to choose size values, order ignored."""
    result, path = [], []

    def explore(start: int) -> None:
        if len(path) == size:
            result.append(path[:])
            return
        for i in range(start, len(values)):
            path.append(values[i])
            explore(i + 1)
            path.pop()

    explore(0)
    return result


def permutations(values: list[int]) -> list[list[int]]:
    """Return every ordering of values."""
    result, path = [], []
    used = [False] * len(values)

    def explore() -> None:
        if len(path) == len(values):
            result.append(path[:])
            return
        for i, value in enumerate(values):
            if used[i]:
                continue
            used[i] = True
            path.append(value)
            explore()
            path.pop()
            used[i] = False

    explore()
    return result
