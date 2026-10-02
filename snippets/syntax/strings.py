def demo_slicing() -> None:
    text = "interview"
    assert text[0] == "i"
    assert text[-1] == "w"
    assert text[2:5] == "ter"
    assert text[:3] == "int"
    assert text[-4:] == "view"
    assert text[::-1] == "weivretni"
    assert text[::2] == "itriw"


def demo_split_join() -> None:
    line = "red, green ,blue"
    assert line.split(",") == ["red", " green ", "blue"]
    parts = [part.strip() for part in line.split(",")]
    assert parts == ["red", "green", "blue"]
    sentence = "  many   spaces here "
    # split() with no argument splits on any whitespace run
    assert sentence.split() == ["many", "spaces", "here"]
    assert "-".join(parts) == "red-green-blue"
    assert ", ".join(map(str, [1, 2, 3])) == "1, 2, 3"
    assert "a1b2".partition("1") == ("a", "1", "b2")


def demo_case_and_checks() -> None:
    assert "Hello".lower() == "hello"
    assert "Hello".upper() == "HELLO"
    assert "abc123".isalnum()
    assert "abc".isalpha()
    assert "123".isdigit()
    assert " \t".isspace()
    assert "Abc"[0].isupper()
    assert "  padded  ".strip() == "padded"
    assert "xxhixx".strip("x") == "hi"
    assert "007".lstrip("0") == "7"


def demo_search() -> None:
    text = "banana"
    assert "nan" in text
    assert text.find("na") == 2
    assert text.find("xyz") == -1
    assert text.rfind("na") == 4
    assert text.index("na") == 2
    assert text.count("a") == 3
    assert text.startswith("ban")
    assert text.endswith(("na", "xyz"))
    assert text.replace("a", "o") == "bonono"
    assert text.replace("a", "o", 1) == "bonana"


def demo_build_strings() -> None:
    # Strings are immutable: collect pieces in a list, join once, O(n)
    pieces = []
    for word in ["fast", "join"]:
        pieces.append(word.upper())
    assert " ".join(pieces) == "FAST JOIN"
    letters = list("cat")
    letters[0] = "b"
    assert "".join(letters) == "bat"
    phrase = "A man, a plan!"
    cleaned = "".join(char.lower() for char in phrase if char.isalnum())
    assert cleaned == "amanaplan"


def demo_letter_counts() -> None:
    counts = [0] * 26
    for char in "abca":
        counts[ord(char) - ord("a")] += 1
    assert counts[:3] == [2, 1, 1]
    # Sorted letters are a key shared by all anagrams
    assert "".join(sorted("listen")) == "eilnst"
    is_anagram = sorted("listen") == sorted("silent")
    assert is_anagram
