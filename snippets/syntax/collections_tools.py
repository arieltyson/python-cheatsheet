from collections import Counter, defaultdict, deque


def demo_deque() -> None:
    queue = deque([1, 2])
    queue.append(3)
    queue.appendleft(0)
    assert queue.popleft() == 0
    assert queue.pop() == 3
    assert queue[0] == 1
    assert list(queue) == [1, 2]
    queue.rotate(1)
    assert list(queue) == [2, 1]
    # maxlen keeps only the newest items
    recent = deque(maxlen=2)
    for value in [1, 2, 3]:
        recent.append(value)
    assert list(recent) == [2, 3]


def demo_defaultdict() -> None:
    groups = defaultdict(list)
    for word in ["eat", "tea", "tan"]:
        groups["".join(sorted(word))].append(word)
    assert groups == {"aet": ["eat", "tea"], "ant": ["tan"]}
    counts = defaultdict(int)
    for char in "aab":
        counts[char] += 1
    assert counts == {"a": 2, "b": 1}
    neighbors = defaultdict(set)
    neighbors[1].add(2)
    assert neighbors[1] == {2}
    # Reading a missing key inserts the default
    assert counts["z"] == 0
    assert "z" in counts


def demo_counter() -> None:
    counts = Counter("banana")
    assert counts == {"a": 3, "n": 2, "b": 1}
    # Missing keys read as 0 and are not inserted
    assert counts["z"] == 0
    assert counts.most_common(2) == [("a", 3), ("n", 2)]
    assert [letter for letter, _ in counts.most_common(2)] == ["a", "n"]
    assert counts.total() == 6
    counts["a"] -= 1
    counts.update("bb")
    assert counts == {"a": 2, "n": 2, "b": 3}
    is_anagram = Counter("listen") == Counter("silent")
    assert is_anagram
    assert Counter("aab") - Counter("ab") == Counter("a")
    assert Counter("ab") + Counter("b") == Counter("abb")
    assert Counter("ab") <= Counter("abc")
