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
