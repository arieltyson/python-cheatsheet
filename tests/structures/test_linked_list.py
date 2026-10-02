import unittest

from snippets.structures.linked_list import (
    ListNode,
    build_list,
    has_cycle,
    list_values,
    merge_sorted,
    middle_node,
    reverse_list,
)


class LinkedListTests(unittest.TestCase):
    def test_build_and_read_round_trip(self) -> None:
        self.assertEqual(list_values(build_list([1, 2, 3])), [1, 2, 3])
        self.assertIsNone(build_list([]))
        self.assertEqual(list_values(None), [])

    def test_reverse(self) -> None:
        cases = [([], []), ([1], [1]), ([1, 2, 3], [3, 2, 1])]
        for values, expected in cases:
            with self.subTest(values=values):
                head = reverse_list(build_list(values))
                self.assertEqual(list_values(head), expected)

    def test_middle(self) -> None:
        self.assertIsNone(middle_node(None))
        self.assertEqual(middle_node(build_list([1])).val, 1)
        self.assertEqual(middle_node(build_list([1, 2, 3])).val, 2)
        self.assertEqual(middle_node(build_list([1, 2, 3, 4])).val, 3)

    def test_cycle(self) -> None:
        self.assertFalse(has_cycle(None))
        self.assertFalse(has_cycle(build_list([1, 2, 3])))
        head = build_list([1, 2, 3])
        head.next.next.next = head.next
        self.assertTrue(has_cycle(head))
        single = ListNode(1)
        single.next = single
        self.assertTrue(has_cycle(single))

    def test_merge_sorted(self) -> None:
        cases = [
            ([], [], []),
            ([1, 3], [], [1, 3]),
            ([1, 4, 5], [1, 2, 6], [1, 1, 2, 4, 5, 6]),
        ]
        for first, second, expected in cases:
            with self.subTest(first=first, second=second):
                merged = merge_sorted(
                    build_list(first), build_list(second)
                )
                self.assertEqual(list_values(merged), expected)


if __name__ == "__main__":
    unittest.main()
