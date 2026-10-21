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


def demo_ord() -> None:
    # Character -> integer code point
    assert ord("a") == 97
    assert ord("A") == 65
    assert ord("0") == 48
    # Letter index in the alphabet: 0 for "a", 25 for "z"
    assert ord("c") - ord("a") == 2
    # Digit character -> int without int()
    assert ord("7") - ord("0") == 7


def demo_chr() -> None:
    # Integer code point -> character (the inverse of ord)
    assert chr(97) == "a"
    assert chr(65) == "A"
    # Alphabet index -> letter
    assert chr(ord("a") + 25) == "z"
    # Shift a letter with wrap-around (Caesar cipher)
    shifted = chr((ord("y") - ord("a") + 3) % 26 + ord("a"))
    assert shifted == "b"
    alphabet = "".join(chr(ord("a") + i) for i in range(26))
    assert alphabet[:5] == "abcde"


def demo_isinstance() -> None:
    assert isinstance(42, int) is True
    assert isinstance("42", int) is False
    # A tuple of types matches any of them
    assert isinstance(3.5, (int, float)) is True
    # Subclasses count: bool is a subclass of int
    flag = True
    assert isinstance(flag, int) is True
    # type() is exact, so it tells a bool from an int
    assert (type(flag) is int) is False

    def flatten(items: list) -> list:
        flat = []
        for item in items:
            if isinstance(item, list):
                flat.extend(flatten(item))
            else:
                flat.append(item)
        return flat

    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


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


def demo_next_iter() -> None:
    numbers = [3, 8, 5, 12]
    # First match, or a default when nothing matches
    assert next((n for n in numbers if n > 6), None) == 8
    assert next((n for n in numbers if n > 99), None) is None
    # Any one item from a set, without removing it
    assert next(iter({7})) == 7
    # iter() makes a one-pass cursor; next() advances it
    cursor = iter(numbers)
    assert next(cursor) == 3
    assert next(cursor) == 8
    assert list(cursor) == [5, 12]
    assert next(cursor, "done") == "done"
    # Subsequence check: each "in" resumes where the last one stopped
    text = iter("abracadabra")
    assert all(char in text for char in "acd") is True


def demo_map_filter() -> None:
    words = ["3", "10", "7"]
    # Both return lazy iterators: wrap in list() to see the values
    assert list(map(int, words)) == [3, 10, 7]
    assert list(map(len, ["hi", "hey"])) == [2, 3]
    evens = filter(lambda n: n % 2 == 0, range(7))
    assert list(evens) == [0, 2, 4, 6]
    # An iterator is single-use: the second pass is empty
    assert list(evens) == []
    # filter(None, ...) drops falsy values: 0, "", None, []
    assert list(filter(None, [0, 1, "", "a", None])) == [1, "a"]
    # The comprehension version is usually clearer
    assert [int(w) for w in words if int(w) > 5] == [10, 7]
