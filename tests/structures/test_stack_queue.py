import unittest

from snippets.structures.stack_queue import is_balanced


class IsBalancedTests(unittest.TestCase):
    def test_balanced(self) -> None:
        for text in ["", "()", "([]{})", "a(b)c", "{[()()]}"]:
            with self.subTest(text=text):
                self.assertTrue(is_balanced(text))

    def test_unbalanced(self) -> None:
        for text in ["(", ")", "(]", "([)]", "(()", "}{"]:
            with self.subTest(text=text):
                self.assertFalse(is_balanced(text))


if __name__ == "__main__":
    unittest.main()
