import unittest

from snippets.structures.lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_missing_key(self) -> None:
        self.assertEqual(LRUCache(1).get(5), -1)

    def test_evicts_least_recently_used(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.put(3, 3)
        self.assertEqual(cache.get(2), -1)
        cache.put(4, 4)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)

    def test_update_refreshes_key(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 10)
        cache.put(3, 3)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), -1)

    def test_capacity_one(self) -> None:
        cache = LRUCache(1)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 2)


if __name__ == "__main__":
    unittest.main()
