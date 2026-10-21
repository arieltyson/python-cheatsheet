from collections import OrderedDict


class LRUCache:
    """Keep the newest capacity keys; evict the least recently used."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        # Oldest key first, most recently used key last
        self.items: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.items:
            return -1
        self.items.move_to_end(key)
        return self.items[key]

    def put(self, key: int, value: int) -> None:
        self.items[key] = value
        self.items.move_to_end(key)
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)


def demo_lru_cache() -> None:
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    # Reading 1 makes it the most recently used
    assert cache.get(1) == 10
    # A third key evicts 2, the least recently used
    cache.put(3, 30)
    assert cache.get(2) == -1
    assert list(cache.items) == [1, 3]
