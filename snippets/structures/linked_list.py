class ListNode:
    __slots__ = ("next", "val")

    def __init__(
        self, val: int = 0, next: "ListNode | None" = None
    ) -> None:
        self.val = val
        self.next = next


def build_list(values: list[int]) -> ListNode | None:
    """Return the head of a linked list holding values in order."""
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_values(head: ListNode | None) -> list[int]:
    """Return the values of a linked list as a Python list."""
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


def reverse_list(head: ListNode | None) -> ListNode | None:
    """Return the new head after reversing the list in place."""
    previous = None
    current = head
    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    return previous


def middle_node(head: ListNode | None) -> ListNode | None:
    """Return the middle node (the second middle for even length)."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def has_cycle(head: ListNode | None) -> bool:
    """Return True if following next pointers ever loops."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def merge_sorted(
    first: ListNode | None, second: ListNode | None
) -> ListNode | None:
    """Return the head of one sorted list made from two sorted lists."""
    dummy = tail = ListNode()
    while first and second:
        if first.val <= second.val:
            tail.next, first = first, first.next
        else:
            tail.next, second = second, second.next
        tail = tail.next
    tail.next = first or second
    return dummy.next
