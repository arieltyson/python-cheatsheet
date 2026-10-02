import heapq


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Return the union of intervals as sorted, non-overlapping ones."""
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Return how many rooms the meetings need at the busiest time."""
    end_times = []
    for start, end in sorted(intervals):
        if end_times and end_times[0] <= start:
            heapq.heapreplace(end_times, end)
        else:
            heapq.heappush(end_times, end)
    return len(end_times)
