import heapq


def demo_min_heap() -> None:
    heap = [5, 1, 4]
    heapq.heapify(heap)
    heapq.heappush(heap, 2)
    # heap[0] is always the smallest item
    assert heap[0] == 1
    assert heapq.heappop(heap) == 1
    assert heapq.heappop(heap) == 2
    # Push then pop in one call: returns the smaller of item and top
    assert heapq.heappushpop(heap, 3) == 3
    # Pop then push in one call
    assert heapq.heapreplace(heap, 0) == 4
    assert sorted(heap) == [0, 5]


def demo_max_heap() -> None:
    heap = []
    for value in [5, 1, 4]:
        heapq.heappush(heap, -value)
    assert -heap[0] == 5
    assert -heapq.heappop(heap) == 5
    assert -heapq.heappop(heap) == 4


def demo_heap_tuples() -> None:
    tasks = []
    heapq.heappush(tasks, (2, "write"))
    heapq.heappush(tasks, (1, "plan"))
    heapq.heappush(tasks, (2, "test"))
    # Equal priorities fall back to comparing the next field
    assert heapq.heappop(tasks) == (1, "plan")
    assert heapq.heappop(tasks) == (2, "test")
    # Dicts cannot be compared: put a unique counter before them
    jobs = []
    for order, job in enumerate([{"id": 7}, {"id": 8}]):
        heapq.heappush(jobs, (1, order, job))
    priority, _, job = heapq.heappop(jobs)
    assert (priority, job) == (1, {"id": 7})


def demo_heap_helpers() -> None:
    scores = [7, 2, 9, 4]
    assert heapq.nlargest(2, scores) == [9, 7]
    assert heapq.nsmallest(2, scores) == [2, 4]
    words = ["bb", "a", "ccc"]
    assert heapq.nlargest(1, words, key=len) == ["ccc"]
    # Merge already-sorted inputs lazily
    assert list(heapq.merge([1, 4], [2, 3])) == [1, 2, 3, 4]
