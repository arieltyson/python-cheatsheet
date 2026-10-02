def demo_range() -> None:
    assert list(range(3)) == [0, 1, 2]
    assert list(range(2, 8, 2)) == [2, 4, 6]
    assert list(range(3, -1, -1)) == [3, 2, 1, 0]


def demo_enumerate_zip() -> None:
    names = ["ada", "bo"]
    scores = [90, 85]
    assert list(enumerate(names)) == [(0, "ada"), (1, "bo")]
    assert list(enumerate(names, start=1)) == [(1, "ada"), (2, "bo")]
    # strict=True raises on unequal lengths (default: stop at shortest)
    pairs = list(zip(names, scores, strict=True))
    assert pairs == [("ada", 90), ("bo", 85)]
    assert dict(pairs) == {"ada": 90, "bo": 85}
    # zip(*pairs) unzips
    unzipped_names, unzipped_scores = zip(*pairs, strict=True)
    assert unzipped_names == ("ada", "bo")
    assert unzipped_scores == (90, 85)


def demo_sorting() -> None:
    words = ["pear", "Fig", "apple"]
    # sorted() returns a new list; uppercase sorts before lowercase
    assert sorted(words) == ["Fig", "apple", "pear"]
    assert sorted(words, key=str.lower) == ["apple", "Fig", "pear"]
    assert sorted(words, key=len) == ["Fig", "pear", "apple"]
    assert sorted(words, reverse=True) == ["pear", "apple", "Fig"]
    # list.sort() sorts in place and returns None
    words.sort()
    assert words == ["Fig", "apple", "pear"]


def demo_sort_keys() -> None:
    people = [("bo", 85), ("ada", 90), ("cy", 85)]
    # Score descending, then name ascending: negate the numeric part
    ranked = sorted(people, key=lambda person: (-person[1], person[0]))
    assert ranked == [("ada", 90), ("bo", 85), ("cy", 85)]
    intervals = [[5, 6], [1, 3], [2, 4]]
    intervals.sort(key=lambda interval: interval[0])
    assert intervals == [[1, 3], [2, 4], [5, 6]]


def demo_min_max() -> None:
    scores = {"ada": 90, "bo": 85}
    assert max(scores, key=scores.get) == "ada"
    assert min([3, 1, 2]) == 1
    assert min(4, 9) == 4
    assert max([], default=0) == 0
    assert min(["banana", "kiwi"], key=len) == "kiwi"


def demo_aggregates() -> None:
    numbers = [3, -1, 4]
    assert sum(numbers) == 6
    assert any(number < 0 for number in numbers)
    assert all(number != 0 for number in numbers)
    assert sum(1 for number in numbers if number > 0) == 2
    assert abs(-7) == 7
    assert divmod(17, 5) == (3, 2)
    assert pow(2, 10, 1000) == 24
    assert list(reversed(numbers)) == [4, -1, 3]


def demo_characters() -> None:
    assert ord("a") == 97
    assert chr(98) == "b"
    assert ord("c") - ord("a") == 2
    assert chr(ord("a") + 25) == "z"


def demo_conversions() -> None:
    assert int("42") == 42
    assert str(42) == "42"
    line = "3 1 2"
    assert list(map(int, line.split())) == [3, 1, 2]
    assert int("1011", 2) == 11
    assert int("ff", 16) == 255
    assert bin(11) == "0b1011"
    assert bin(11)[2:] == "1011"
    assert hex(255) == "0xff"
