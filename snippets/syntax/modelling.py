from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from functools import reduce
from operator import attrgetter


@dataclass(frozen=True)
class Note:
    """frozen=True: fields can't change, so == AND hash() both work."""

    id: int
    text: str


def demo_equality() -> None:
    saved = Note(1, "Milk")
    draft = replace(saved, text="Oat milk")  # a changed copy
    # @dataclass writes __eq__: every field must match
    assert Note(1, "Milk") == saved
    assert draft.id == saved.id
    assert draft != saved
    # Lists compare element by element, in order
    assert [saved, draft] != [draft, saved]
    # frozen dataclasses are hashable: sets and dict keys work
    assert len({saved, saved, draft}) == 2
    # A plain class compares by identity until you write __eq__
    assert object() != object()


class Shelf:
    """Callers read the data but can only change it through add()."""

    def __init__(self) -> None:
        self._pages: dict[str, int] = {}  # _ means "internal"

    @property
    def titles(self) -> tuple[str, ...]:
        return tuple(self._pages)  # a tuple: callers can't append

    @property
    def total_pages(self) -> int:
        return sum(self._pages.values())  # computed on every read

    def add(self, title: str, pages: int) -> None:
        self._pages[title] = pages


def demo_read_only() -> None:
    shelf = Shelf()
    shelf.add("Dune", 412)
    shelf.add("Emma", 474)
    assert shelf.titles == ("Dune", "Emma")
    assert shelf.total_pages == 886
    # shelf.titles = ()      AttributeError: property has no setter
    # shelf.titles.append()  AttributeError: tuples are immutable


@dataclass(frozen=True)
class Profile:
    name: str
    city: str

    def updated(
        self, *, name: str | None = None, city: str | None = None
    ) -> "Profile":
        return Profile(
            name=self.name if name is None else name,
            city=self.city if city is None else city,
        )


def demo_optional_parameters() -> None:
    ada = Profile("Ada", "London")
    moved = ada.updated(city="Paris")  # pass only what changes
    assert moved.name == "Ada"
    assert moved.city == "Paris"
    assert ada.updated() == ada  # nothing passed, nothing changed
    # `name or self.name` would wrongly ignore "" and 0: test for None


def demo_update_in_place() -> None:
    songs = [Note(1, "Hey"), Note(2, "Yo")]
    # Find the position by id; next(..., None) when it may be missing
    index = next((i for i, s in enumerate(songs) if s.id == 2), None)
    assert index == 1
    songs[index] = replace(songs[index], text="Yo!")
    assert [s.text for s in songs] == ["Hey", "Yo!"]
    assert len(songs) == 2  # updated, not duplicated
    missing = next((i for i, s in enumerate(songs) if s.id == 9), None)
    assert missing is None  # unknown id: nothing to change
    del songs[0]  # delete by position
    assert [s.id for s in songs] == [2]


def demo_sum_by_key() -> None:
    sales = [("Food", 450), ("Travel", 1200), ("Food", 300)]
    totals: defaultdict[str, int] = defaultdict(int)
    for category, cents in sales:
        totals[category] += cents  # a missing key starts at 0
    assert totals == {"Food": 750, "Travel": 1200}
    # Without defaultdict: dict.get with a default
    plain: dict[str, int] = {}
    for category, cents in sales:
        plain[category] = plain.get(category, 0) + cents
    assert plain == totals
    # Counter adds per key too
    assert Counter({"Food": 450}) + Counter({"Food": 300}) == {
        "Food": 750
    }
    # Transform every value, keep the keys
    assert {k: v // 100 for k, v in plain.items()} == {
        "Food": 7,
        "Travel": 12,
    }
    del plain["Travel"]  # remove the key, don't leave a 0 behind
    assert plain == {"Food": 750}


@dataclass
class Purchase:
    item: str
    cents: int
    returned: bool = False


def demo_reduce() -> None:
    cart = [Purchase("Tea", 300), Purchase("Jam", 450)]
    # The usual way: sum over a generator
    assert sum(p.cents for p in cart) == 750
    # reduce(fn, items, start): fn gets (running result, next item)
    # and returns the new running result. Steps: 0+300, then 300+450
    total = reduce(lambda running, p: running + p.cents, cart, 0)
    assert total == 750
    assert sum(p.cents for p in []) == 0  # empty: the start value


def demo_attribute_map() -> None:
    cart = [Purchase("Tea", 300), Purchase("Jam", 450, returned=True)]
    # A comprehension builds a NEW list: one output per item, in order
    assert [p.item for p in cart] == ["Tea", "Jam"]
    # attrgetter("item") is a function that reads .item from anything
    assert list(map(attrgetter("item"), cart)) == ["Tea", "Jam"]
    assert [p.item for p in cart if p.returned] == ["Jam"]
    assert any(p.returned for p in cart)
    # attrgetter also works as a sort key
    by_price = sorted(cart, key=attrgetter("cents"), reverse=True)
    assert [p.item for p in by_price] == ["Jam", "Tea"]
