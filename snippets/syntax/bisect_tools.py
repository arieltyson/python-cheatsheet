import bisect


def demo_bisect() -> None:
    values = [1, 3, 3, 3, 7]
    # bisect_left: first index with value >= target
    assert bisect.bisect_left(values, 3) == 1
    # bisect_right: first index with value > target
    assert bisect.bisect_right(values, 3) == 4
    assert bisect.bisect_left(values, 8) == 5
    # Is 5 present? Check the slot bisect_left points at
    i = bisect.bisect_left(values, 5)
    assert (i < len(values) and values[i] == 5) is False
    # Count values in [2, 6]
    low = bisect.bisect_left(values, 2)
    assert bisect.bisect_right(values, 6) - low == 3
    bisect.insort(values, 4)
    assert values == [1, 3, 3, 3, 4, 7]


def demo_bisect_key() -> None:
    # key= (Python 3.10+) searches records sorted by one field
    events = [(1, "boot"), (4, "login"), (9, "logout")]
    index = bisect.bisect_right(events, 5, key=lambda e: e[0]) - 1
    # The latest event at or before time 5
    assert events[index] == (4, "login")
