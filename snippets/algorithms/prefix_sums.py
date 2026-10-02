from collections import Counter


def prefix_sums(values: list[int]) -> list[int]:
    """Return sums where prefix[i] is the sum of values[:i]."""
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    return prefix


def demo_range_sum() -> None:
    prefix = prefix_sums([3, 1, 4, 1])
    assert prefix == [0, 3, 4, 8, 9]
    # Sum of values[left..right] inclusive, in O(1)
    left, right = 1, 3
    assert prefix[right + 1] - prefix[left] == 6


def count_subarrays_with_sum(values: list[int], target: int) -> int:
    """Return how many contiguous subarrays sum to target."""
    seen = Counter({0: 1})
    running = count = 0
    for value in values:
        running += value
        count += seen[running - target]
        seen[running] += 1
    return count
