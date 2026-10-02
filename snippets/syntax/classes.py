import heapq


class Task:
    """A record that sorts by priority, then name."""

    __slots__ = ("name", "priority")

    def __init__(self, priority: int, name: str) -> None:
        self.priority = priority
        self.name = name

    def __lt__(self, other: "Task") -> bool:
        return (self.priority, self.name) < (other.priority, other.name)

    def __repr__(self) -> str:
        return f"Task({self.priority!r}, {self.name!r})"


def demo_task() -> None:
    tasks = [Task(2, "write"), Task(1, "plan")]
    # __lt__ is all that sorted() and heapq need
    heapq.heapify(tasks)
    assert heapq.heappop(tasks).name == "plan"
    assert sorted([Task(3, "b"), Task(3, "a")])[0].name == "a"
    assert repr(Task(1, "plan")) == "Task(1, 'plan')"
