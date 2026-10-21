from itertools import (
    accumulate,
    chain,
    combinations,
    groupby,
    pairwise,
    permutations,
    product,
)


def demo_running_totals() -> None:
    assert list(accumulate([3, 1, 4])) == [3, 4, 8]
    # initial=0 gives prefix sums ready for range queries
    assert list(accumulate([3, 1, 4], initial=0)) == [0, 3, 4, 8]
    # Any two-argument function: running max
    assert list(accumulate([3, 1, 4], max)) == [3, 3, 4]
    assert list(pairwise([1, 4, 9])) == [(1, 4), (4, 9)]
    gaps = [b - a for a, b in pairwise([1, 4, 9])]
    assert gaps == [3, 5]


def demo_combinatorics() -> None:
    pairs = list(combinations("abc", 2))
    assert pairs == [("a", "b"), ("a", "c"), ("b", "c")]
    assert len(list(permutations([1, 2, 3]))) == 6
    assert list(permutations("ab")) == [("a", "b"), ("b", "a")]
    bits = list(product([0, 1], repeat=2))
    assert bits == [(0, 0), (0, 1), (1, 0), (1, 1)]
    # Every cell of a grid without nested loops
    cells = list(product(range(2), range(3)))
    assert len(cells) == 6


def demo_groupby_chain() -> None:
    runs = [(key, len(list(group))) for key, group in groupby("aaabcc")]
    assert runs == [("a", 3), ("b", 1), ("c", 2)]
    encoded = "".join(
        f"{k}{len(list(g))}" for k, g in groupby("aaabcc")
    )
    assert encoded == "a3b1c2"
    # groupby only merges neighbours: sort first to group everything
    assert [k for k, _ in groupby("abab")] == ["a", "b", "a", "b"]
    assert [k for k, _ in groupby(sorted("abab"))] == ["a", "b"]
    assert list(chain([1, 2], [3])) == [1, 2, 3]
    nested = [[1], [2, 3]]
    assert list(chain.from_iterable(nested)) == [1, 2, 3]
