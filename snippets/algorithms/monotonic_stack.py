def next_greater(values: list[int]) -> list[int]:
    """Return the next larger value to the right of each item, or -1."""
    result = [-1] * len(values)
    # Indices still waiting for a larger value; their values decrease
    waiting = []
    for i, value in enumerate(values):
        while waiting and values[waiting[-1]] < value:
            result[waiting.pop()] = value
        waiting.append(i)
    return result
