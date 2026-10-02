import heapq


def merge_sort(values: list[int]) -> list[int]:
    """Return a new sorted list (stable)."""
    if len(values) <= 1:
        return values[:]
    middle = len(values) // 2
    left, right = (
        merge_sort(values[:middle]),
        merge_sort(values[middle:]),
    )
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def kth_largest(values: list[int], k: int) -> int:
    """Return the k-th largest value (k = 1 is the maximum)."""
    candidates = values
    while True:
        pivot = candidates[len(candidates) // 2]
        larger = [value for value in candidates if value > pivot]
        equal = sum(1 for value in candidates if value == pivot)
        if k <= len(larger):
            candidates = larger
        elif k <= len(larger) + equal:
            return pivot
        else:
            k -= len(larger) + equal
            candidates = [
                value for value in candidates if value < pivot
            ]


def top_k_largest(values: list[int], k: int) -> list[int]:
    """Return the k largest values, largest first."""
    # Min-heap of the best k so far; heap[0] is the weakest of them
    heap = []
    for value in values:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif heap and value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)
