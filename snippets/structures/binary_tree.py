import math
from collections import deque


class TreeNode:
    __slots__ = ("left", "right", "val")

    def __init__(
        self,
        val: int = 0,
        left: "TreeNode | None" = None,
        right: "TreeNode | None" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: list[int | None]) -> TreeNode | None:
    """Return the root of a tree given in level order, None = gap."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    index = 1
    while queue and index < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if index < len(values) and values[index] is not None:
                child = TreeNode(values[index])
                setattr(node, side, child)
                queue.append(child)
            index += 1
    return root


def traversals(
    root: TreeNode | None,
) -> tuple[list[int], list[int], list[int]]:
    """Return the (preorder, inorder, postorder) values."""
    preorder, inorder, postorder = [], [], []

    def visit(node: TreeNode | None) -> None:
        if node is None:
            return
        preorder.append(node.val)
        visit(node.left)
        inorder.append(node.val)
        visit(node.right)
        postorder.append(node.val)

    visit(root)
    return preorder, inorder, postorder


def inorder_iterative(root: TreeNode | None) -> list[int]:
    """Return inorder values without recursion."""
    values, stack = [], []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        values.append(node.val)
        node = node.right
    return values


def level_order(root: TreeNode | None) -> list[list[int]]:
    """Return the values of each level, top to bottom."""
    levels = []
    queue = deque([root] if root else [])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels


def max_depth(root: TreeNode | None) -> int:
    """Return the number of nodes on the longest root-to-leaf path."""
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def bst_search(root: TreeNode | None, target: int) -> TreeNode | None:
    """Return the node holding target, or None."""
    node = root
    while node and node.val != target:
        node = node.left if target < node.val else node.right
    return node


def bst_insert(root: TreeNode | None, val: int) -> TreeNode:
    """Insert val and return the (possibly new) root."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root


def is_valid_bst(
    root: TreeNode | None,
    low: float = -math.inf,
    high: float = math.inf,
) -> bool:
    """Return True if every node is strictly between its bounds."""
    if root is None:
        return True
    if not low < root.val < high:
        return False
    left_valid = is_valid_bst(root.left, low, root.val)
    return left_valid and is_valid_bst(root.right, root.val, high)
