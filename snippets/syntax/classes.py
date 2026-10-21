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


def demo_attributes() -> None:
    task = Task(1, "plan")
    field = "priority"
    assert getattr(task, field) == 1
    setattr(task, field, 5)
    assert task.priority == 5
    # A default avoids AttributeError for a missing attribute
    assert getattr(task, "owner", None) is None
    assert hasattr(task, "owner") is False
    # Dispatch by name: look up a method, check it, then call it
    command = "upper"
    method = getattr("ship it", command, None)
    assert callable(method) is True
    assert method() == "SHIP IT"
