from collections import deque


def demo_stack() -> None:
    stack = []
    stack.append(1)
    stack.append(2)
    assert stack[-1] == 2
    assert stack.pop() == 2
    assert stack == [1]
    # Empty containers are falsy
    stack.pop()
    assert not stack


def demo_queue() -> None:
    queue = deque()
    queue.append("first")
    queue.append("second")
    assert queue[0] == "first"
    assert queue.popleft() == "first"
    assert len(queue) == 1


def demo_ring_buffer() -> None:
    # maxlen makes a deque drop the oldest item when it is full
    ring = deque(maxlen=3)
    for value in range(1, 6):
        ring.append(value)
    assert list(ring) == [3, 4, 5]
    assert len(ring) == 3


def is_balanced(text: str) -> bool:
    """Return True if every bracket in text closes in order."""
    opening_for = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in opening_for:
            expected = opening_for[char]
            if not stack or stack.pop() != expected:
                return False
    return not stack
