import unittest

from snippets.structures.trie import Trie
from snippets.structures.union_find import UnionFind


class TrieTests(unittest.TestCase):
    def test_empty_trie(self) -> None:
        words = Trie()
        self.assertFalse(words.search("a"))
        self.assertTrue(words.starts_with(""))
        self.assertFalse(words.search(""))

    def test_words_and_prefixes(self) -> None:
        words = Trie()
        for word in ["car", "card", "care", "dog"]:
            words.insert(word)
        self.assertTrue(words.search("card"))
        self.assertFalse(words.search("ca"))
        self.assertTrue(words.starts_with("ca"))
        self.assertFalse(words.starts_with("cat"))
        self.assertFalse(words.search("cards"))

    def test_empty_word(self) -> None:
        words = Trie()
        words.insert("")
        self.assertTrue(words.search(""))


class UnionFindTests(unittest.TestCase):
    def test_components(self) -> None:
        groups = UnionFind(5)
        self.assertEqual(groups.components, 5)
        for first, second in [(0, 1), (1, 2), (3, 4)]:
            self.assertTrue(groups.union(first, second))
        self.assertEqual(groups.components, 2)
        self.assertEqual(groups.find(0), groups.find(2))
        self.assertNotEqual(groups.find(0), groups.find(3))

    def test_redundant_edge(self) -> None:
        groups = UnionFind(3)
        edges = [(0, 1), (1, 2), (2, 0)]
        redundant = [edge for edge in edges if not groups.union(*edge)]
        self.assertEqual(redundant, [(2, 0)])

    def test_long_chain_does_not_recurse(self) -> None:
        count = 100_000
        groups = UnionFind(count)
        for node in range(1, count):
            groups.union(node - 1, node)
        self.assertEqual(groups.components, 1)
        self.assertEqual(groups.find(count - 1), groups.find(0))


if __name__ == "__main__":
    unittest.main()
