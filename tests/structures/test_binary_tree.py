import unittest

from snippets.structures.binary_tree import (
    TreeNode,
    bst_insert,
    bst_search,
    build_tree,
    inorder_iterative,
    is_valid_bst,
    level_order,
    max_depth,
    traversals,
)

#       4
#     2   6
#    1 3 5 7
BALANCED = [4, 2, 6, 1, 3, 5, 7]


class BuildTreeTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertIsNone(build_tree([]))
        self.assertIsNone(build_tree([None]))

    def test_gaps(self) -> None:
        root = build_tree([1, None, 2, 3])
        self.assertIsNone(root.left)
        self.assertEqual(root.right.val, 2)
        self.assertEqual(root.right.left.val, 3)


class TraversalTests(unittest.TestCase):
    def test_three_orders(self) -> None:
        preorder, inorder, postorder = traversals(build_tree(BALANCED))
        self.assertEqual(preorder, [4, 2, 1, 3, 6, 5, 7])
        self.assertEqual(inorder, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(postorder, [1, 3, 2, 5, 7, 6, 4])

    def test_empty_tree(self) -> None:
        self.assertEqual(traversals(None), ([], [], []))
        self.assertEqual(inorder_iterative(None), [])
        self.assertEqual(level_order(None), [])
        self.assertEqual(max_depth(None), 0)

    def test_iterative_matches_recursive(self) -> None:
        for values in (BALANCED, [1, None, 2, 3], [5, 3, None, 2]):
            with self.subTest(values=values):
                root = build_tree(values)
                self.assertEqual(
                    inorder_iterative(root), traversals(root)[1]
                )

    def test_level_order(self) -> None:
        self.assertEqual(
            level_order(build_tree(BALANCED)),
            [[4], [2, 6], [1, 3, 5, 7]],
        )

    def test_max_depth(self) -> None:
        self.assertEqual(max_depth(build_tree(BALANCED)), 3)
        self.assertEqual(
            max_depth(build_tree([1, None, 2, None, 3])), 3
        )


class BinarySearchTreeTests(unittest.TestCase):
    def test_search(self) -> None:
        root = build_tree(BALANCED)
        self.assertEqual(bst_search(root, 5).val, 5)
        self.assertIsNone(bst_search(root, 8))
        self.assertIsNone(bst_search(None, 1))

    def test_insert_keeps_order(self) -> None:
        root = None
        for value in [5, 3, 8, 1, 4, 9]:
            root = bst_insert(root, value)
        self.assertEqual(traversals(root)[1], [1, 3, 4, 5, 8, 9])
        self.assertTrue(is_valid_bst(root))

    def test_validate(self) -> None:
        self.assertTrue(is_valid_bst(None))
        self.assertTrue(is_valid_bst(build_tree(BALANCED)))
        # 4 sits in the right subtree of 5, so it breaks the bound
        self.assertFalse(
            is_valid_bst(build_tree([5, 1, 6, None, None, 4, 7]))
        )
        self.assertFalse(is_valid_bst(TreeNode(2, TreeNode(2))))


if __name__ == "__main__":
    unittest.main()
