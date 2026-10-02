def demo_range() -> None:
    assert list(range(3)) == [0, 1, 2]
    assert list(range(2, 8, 2)) == [2, 4, 6]
    assert list(range(3, -1, -1)) == [3, 2, 1, 0]
