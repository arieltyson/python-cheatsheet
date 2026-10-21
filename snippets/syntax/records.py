from dataclasses import FrozenInstanceError, dataclass, field


@dataclass(order=True)
class Transaction:
    """A ledger row. order=True sorts by the fields, top to bottom."""

    timestamp: int
    amount_cents: int
    merchant: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Point:
    """Immutable and hashable, so it works as a dict key."""

    row: int
    col: int


def demo_dataclass() -> None:
    first = Transaction(1, 2500, "cafe")
    later = Transaction(2, 900, "taxi")
    # __init__, __repr__ and __eq__ are written for you
    assert first == Transaction(1, 2500, "cafe")
    assert sorted([later, first])[0] is first
    # default_factory gives every row its own list
    first.tags.append("food")
    assert later.tags == []
    seen = {Point(0, 1)}
    assert (Point(0, 1) in seen) is True
    error = ""
    try:
        Point(0, 1).row = 5
    except FrozenInstanceError as e:
        error = type(e).__name__
    assert error == "FrozenInstanceError"
