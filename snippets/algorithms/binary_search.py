from collections.abc import Callable


def binary_search(values: list[int], target: int) -> int:
    """Return an index of target in sorted values, or -1."""
    low, high = 0, len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def lower_bound(values: list[int], target: int) -> int:
    """Return the first index with value >= target (len if none)."""
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low


def upper_bound(values: list[int], target: int) -> int:
    """Return the first index with value > target (len if none)."""
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] <= target:
            low = middle + 1
        else:
            high = middle
    return low


def first_true(
    low: int, high: int, is_valid: Callable[[int], bool]
) -> int:
    """Return the smallest x in [low, high] with is_valid(x) True.

    is_valid must be False, ..., False, True, ..., True over the range,
    and is_valid(high) must be True.
    """
    while low < high:
        middle = (low + high) // 2
        if is_valid(middle):
            high = middle
        else:
            low = middle + 1
    return low


def min_eating_speed(piles: list[int], hours: int) -> int:
    """Return the slowest speed that finishes every pile in time."""

    def can_finish(speed: int) -> bool:
        return sum(-(-pile // speed) for pile in piles) <= hours

    return first_true(1, max(piles), can_finish)
