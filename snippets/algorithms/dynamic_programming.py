def climb_stairs_memo(steps: int) -> int:
    """Return the ways to climb taking 1 or 2 steps (top-down)."""
    memo = {0: 1, 1: 1}

    def ways(remaining: int) -> int:
        if remaining not in memo:
            memo[remaining] = ways(remaining - 1) + ways(remaining - 2)
        return memo[remaining]

    return ways(steps)


def climb_stairs(steps: int) -> int:
    """Return the ways to climb taking 1 or 2 steps (bottom-up)."""
    previous, current = 1, 1
    for _ in range(steps - 1):
        previous, current = current, previous + current
    return current


def house_robber(values: list[int]) -> int:
    """Return the largest sum with no two adjacent values taken."""
    # Best totals up to two houses back and up to the previous house
    previous, current = 0, 0
    for value in values:
        previous, current = current, max(current, previous + value)
    return current


def coin_change(coins: list[int], amount: int) -> int:
    """Return the fewest coins that sum to amount, or -1."""
    impossible = amount + 1
    fewest = [0] + [impossible] * amount
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                fewest[total] = min(
                    fewest[total], fewest[total - coin] + 1
                )
    return fewest[amount] if fewest[amount] != impossible else -1


def knapsack(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the best total value with each item used at most once."""
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values, strict=True):
        # Go downward so each item is counted at most once
        for room in range(capacity, weight - 1, -1):
            best[room] = max(best[room], best[room - weight] + value)
    return best[capacity]


def unique_grid_paths(rows: int, cols: int) -> int:
    """Return the right/down paths from top-left to bottom-right."""
    row = [1] * cols
    for _ in range(1, rows):
        for col in range(1, cols):
            row[col] += row[col - 1]
    return row[-1]


def longest_common_subsequence(first: str, second: str) -> int:
    """Return the length of the longest common subsequence."""
    table = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i, first_char in enumerate(first, start=1):
        for j, second_char in enumerate(second, start=1):
            if first_char == second_char:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[-1][-1]


def longest_increasing_subsequence(values: list[int]) -> int:
    """Return the length of the longest strictly rising subsequence."""
    # tails[k] = smallest tail of any increasing run of length k + 1
    tails = []
    for value in values:
        low, high = 0, len(tails)
        while low < high:
            middle = (low + high) // 2
            if tails[middle] < value:
                low = middle + 1
            else:
                high = middle
        if low == len(tails):
            tails.append(value)
        else:
            tails[low] = value
    return len(tails)
