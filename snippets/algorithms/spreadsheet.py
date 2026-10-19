from collections import defaultdict


def parse_expression(expression: str) -> tuple[int, list[str]]:
    """Split "=A1+B2+5" into (5, ["A1", "B2"]); "42" into (42, [])."""
    if not expression.startswith("="):
        return int(expression), []
    constant, refs = 0, []
    for term in expression[1:].split("+"):
        name = term.strip()
        if name.isdigit():
            constant += int(name)
        else:
            refs.append(name)
    return constant, refs


class Spreadsheet:
    """Parts 1 and 2: evaluate on read, detect cycles on read."""

    def __init__(self) -> None:
        self.cells: dict[str, tuple[int, list[str]]] = {}

    def set_cell(self, key: str, expression: str) -> None:
        self.cells[key] = parse_expression(expression)

    def get_cell(self, key: str) -> int:
        return self._evaluate(key, set(), {})

    def _evaluate(
        self, key: str, visiting: set[str], values: dict[str, int]
    ) -> int:
        if key in values:
            return values[key]
        if key in visiting:  # key is already on the current path
            raise ValueError("Cycle detected")
        constant, refs = self.cells.get(key, (0, []))
        visiting.add(key)
        total = constant
        for ref in refs:
            total += self._evaluate(ref, visiting, values)
        visiting.remove(key)
        values[key] = total
        return total


def demo_spreadsheet() -> None:
    sheet = Spreadsheet()
    sheet.set_cell("A1", "10")
    sheet.set_cell("B1", "=A1+5")
    sheet.set_cell("C1", "=A1 + B1 + 2")
    assert sheet.get_cell("C1") == 27
    assert sheet.get_cell("Z9") == 0  # never set
    sheet.set_cell("A1", "=C1+1")  # A1 -> C1 -> B1 -> A1
    message = ""
    try:
        sheet.get_cell("C1")
    except ValueError as e:
        message = f"Error found: {e}"  # or print(f"...")
    assert message == "Error found: Cycle detected"
    sheet.set_cell("A1", "4")
    assert sheet.get_cell("C1") == 15


class CachedSpreadsheet:
    """Part 3: O(1) repeated reads; a write clears only downstream."""

    def __init__(self) -> None:
        self.cells: dict[str, tuple[int, list[str]]] = {}
        # dependents["A1"] = cells whose formulas mention A1
        self.dependents: defaultdict[str, set[str]] = defaultdict(set)
        self.cache: dict[str, int] = {}

    def set_cell(self, key: str, expression: str) -> None:
        constant, refs = parse_expression(expression)
        if self._reaches(refs, key):  # reject before changing state
            raise ValueError("Cycle detected")
        for ref in self._refs(key):
            self.dependents[ref].discard(key)
        for ref in refs:
            self.dependents[ref].add(key)
        self.cells[key] = (constant, refs)
        self._invalidate(key)

    def get_cell(self, key: str) -> int:
        if key not in self.cache:
            constant, refs = self.cells.get(key, (0, []))
            total = constant + sum(self.get_cell(ref) for ref in refs)
            self.cache[key] = total
        return self.cache[key]

    def _refs(self, key: str) -> list[str]:
        return self.cells.get(key, (0, []))[1]

    def _reaches(self, starts: list[str], target: str) -> bool:
        """Is target reachable from starts by following references?"""
        stack, seen = list(starts), set(starts)
        while stack:
            node = stack.pop()
            if node == target:
                return True
            for ref in self._refs(node):
                if ref not in seen:
                    seen.add(ref)
                    stack.append(ref)
        return False

    def _invalidate(self, key: str) -> None:
        """Drop key and every cell downstream of it from the cache."""
        stack, seen = [key], {key}
        while stack:
            node = stack.pop()
            self.cache.pop(node, None)
            for dependent in self.dependents[node]:
                if dependent not in seen:
                    seen.add(dependent)
                    stack.append(dependent)


def demo_cached_spreadsheet() -> None:
    sheet = CachedSpreadsheet()
    sheet.set_cell("A1", "10")
    sheet.set_cell("B1", "=A1+5")
    sheet.set_cell("C1", "=A1+B1+2")
    assert sheet.get_cell("C1") == 27
    assert sheet.cache == {"A1": 10, "B1": 15, "C1": 27}
    sheet.set_cell("D1", "1")  # nothing depends on D1
    assert sheet.cache == {"A1": 10, "B1": 15, "C1": 27}
    sheet.set_cell("A1", "20")  # clears A1, B1 and C1
    assert sheet.cache == {}
    assert sheet.get_cell("C1") == 47
    message = ""
    try:
        sheet.set_cell("A1", "=C1+1")
    except ValueError as e:
        message = f"Error found: {e}"
    assert message == "Error found: Cycle detected"
    # The rejected write changed nothing
    assert sheet.get_cell("C1") == 47
