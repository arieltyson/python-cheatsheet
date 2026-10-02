def demo_bits() -> None:
    value = 0b1100
    assert value & 1 == 0
    assert value >> 2 == 0b11
    assert (value >> 3) & 1 == 1
    assert value | (1 << 0) == 0b1101
    assert value ^ (1 << 2) == 0b1000
    # Clear the lowest set bit, and isolate it
    assert value & (value - 1) == 0b1000
    assert value & -value == 0b100
    assert value.bit_count() == 2
    assert value.bit_length() == 4
    is_power_of_two = value > 0 and value & (value - 1) == 0
    assert is_power_of_two is False


def demo_bitmask_subsets() -> None:
    items = ["a", "b", "c"]
    subsets = [
        [item for i, item in enumerate(items) if mask >> i & 1]
        for mask in range(1 << len(items))
    ]
    assert len(subsets) == 8
    assert subsets[0b101] == ["a", "c"]


def single_number(values: list[int]) -> int:
    """Return the value that appears once when the rest appear twice."""
    result = 0
    for value in values:
        result ^= value
    return result
