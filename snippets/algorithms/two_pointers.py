def pair_with_sum(
    values: list[int], target: int
) -> tuple[int, int] | None:
    """Return indices of two sorted values adding to target, or None."""
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def three_sum(values: list[int]) -> list[list[int]]:
    """Return every unique triplet that sums to zero."""
    ordered = sorted(values)
    triplets = []
    for i in range(len(ordered) - 2):
        if i > 0 and ordered[i] == ordered[i - 1]:
            continue
        left, right = i + 1, len(ordered) - 1
        while left < right:
            total = ordered[i] + ordered[left] + ordered[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                triplets.append(
                    [ordered[i], ordered[left], ordered[right]]
                )
                left += 1
                right -= 1
                while (
                    left < right and ordered[left] == ordered[left - 1]
                ):
                    left += 1
    return triplets


def remove_duplicates(values: list[int]) -> int:
    """Dedupe sorted values in place and return the new length."""
    write = 0
    for value in values:
        if write == 0 or value != values[write - 1]:
            values[write] = value
            write += 1
    return write


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same both ways (letters only)."""
    left, right = 0, len(text) - 1
    while left < right:
        if not text[left].isalnum():
            left += 1
        elif not text[right].isalnum():
            right -= 1
        elif text[left].lower() != text[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True
