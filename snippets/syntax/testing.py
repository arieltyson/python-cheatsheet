import math


def demo_assert() -> None:
    total = 2 + 3
    assert total == 5, "addition is broken"
    assert total == 5, f"expected 5, got {total}"
    # A failing assert raises AssertionError with your message
    message = ""
    try:
        assert total == 6, f"expected 6, got {total}"
    except AssertionError as e:
        message = str(e)
    assert message == "expected 6, got 5", message
    # Long message: wrap only the message in parentheses
    assert total > 0, (
        f"total should be positive after adding 2 and 3, got {total}"
    )


def demo_assert_shapes() -> None:
    result = [3, 1, 2]
    assert sorted(result) == [1, 2, 3], "same items, any order"
    assert set(result) == {1, 2, 3}, "same unique items"
    assert len(result) == 3, f"wrong length: {len(result)}"
    assert 2 in result, "2 is missing"
    assert result is not None, "function returned None"
    assert math.isclose(0.1 + 0.2, 0.3), "compare floats with isclose"
    cache = {"C1": 30}
    assert "C1" in cache, "C1 should be cached"
    assert "A1" not in cache, "A1 should not be cached"


def demo_assert_raises() -> None:
    def get_cell(key: str) -> int:
        raise ValueError("Cycle detected")

    try:
        get_cell("C1")
    except ValueError as e:
        assert str(e) == "Cycle detected", f"wrong message: {e}"
    else:
        raise AssertionError("expected ValueError")
    # print("All tests passed") after the last check
