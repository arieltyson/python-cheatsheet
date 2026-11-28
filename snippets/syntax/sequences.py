from bisect import insort


def demo_find_and_insert() -> None:
    scores = [90, 70, 50]  # kept high to low
    # list.index finds an equal value, and RAISES when it is missing
    assert scores.index(70) == 1
    # next() over a generator finds the first match, or a default
    assert next((i for i, s in enumerate(scores) if s <= 60), None) == 2
    missing = next((i for i, s in enumerate(scores) if s <= 10), None)
    assert missing is None
    # insert(i, x) puts x AT index i and shifts the rest right.
    # Index len(list) is one past the end, so inserting there appends.
    at = next((i for i, s in enumerate(scores) if s <= 60), len(scores))
    scores.insert(at, 60)
    assert scores == [90, 70, 60, 50]
    scores.insert(len(scores), 10)
    assert scores == [90, 70, 60, 50, 10]
    # Ascending lists: insort finds the spot by binary search
    ascending = [10, 30]
    insort(ascending, 20)
    assert ascending == [10, 20, 30]


def demo_zip() -> None:
    names = ["ada", "bo"]
    scores = [90, 85, 70]
    # zip pairs items by position and STOPS at the shorter list
    assert list(zip(names, scores)) == [("ada", 90), ("bo", 85)]
    lines = [
        f"{name} scored {score}" for name, score in zip(names, scores)
    ]
    assert lines == ["ada scored 90", "bo scored 85"]
    # Each pair is a tuple: [0] from the first list, [1] the second
    first = next(zip(names, scores))
    assert first[0] == "ada"
    assert first[1] == 90
    assert dict(zip(names, scores)) == {"ada": 90, "bo": 85}
    # Neighbours: zip a list with itself shifted by one
    assert [a - b for a, b in zip(scores, scores[1:])] == [5, 15]
