class UnionFind:
    __slots__ = ("components", "parent", "size")

    def __init__(self, count: int) -> None:
        self.parent = list(range(count))
        self.size = [1] * count
        self.components = count

    def find(self, node: int) -> int:
        # Path halving: point each visited node at its grandparent
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, first: int, second: int) -> bool:
        """Join two sets; return False if already in the same set."""
        root_first, root_second = self.find(first), self.find(second)
        if root_first == root_second:
            return False
        if self.size[root_first] < self.size[root_second]:
            root_first, root_second = root_second, root_first
        self.parent[root_second] = root_first
        self.size[root_first] += self.size[root_second]
        self.components -= 1
        return True


def demo_union_find() -> None:
    groups = UnionFind(4)
    assert groups.union(0, 1) is True
    assert groups.union(2, 3) is True
    # Already connected: in an edge list this edge closes a cycle
    assert groups.union(1, 0) is False
    assert groups.find(0) == groups.find(1)
    assert groups.components == 2
