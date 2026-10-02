from collections import defaultdict


def max_window_sum(values: list[int], size: int) -> int:
    """Return the largest sum of `size` consecutive values."""
    window = sum(values[:size])
    best = window
    for end in range(size, len(values)):
        window += values[end] - values[end - size]
        best = max(best, window)
    return best


def longest_with_k_distinct(text: str, k: int) -> int:
    """Return the longest substring length with at most k distinct."""
    counts = defaultdict(int)
    start = best = 0
    for end, char in enumerate(text):
        counts[char] += 1
        while len(counts) > k:
            counts[text[start]] -= 1
            if counts[text[start]] == 0:
                del counts[text[start]]
            start += 1
        best = max(best, end - start + 1)
    return best


def longest_unique_substring(text: str) -> int:
    """Return the longest substring length with no repeated chars."""
    last_seen: dict[str, int] = {}
    start = best = 0
    for end, char in enumerate(text):
        if last_seen.get(char, -1) >= start:
            start = last_seen[char] + 1
        last_seen[char] = end
        best = max(best, end - start + 1)
    return best
