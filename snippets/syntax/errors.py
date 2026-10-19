class CycleError(ValueError):
    """Subclass ValueError so `except ValueError` still catches it."""


def demo_try_except() -> None:
    try:
        number = int("abc")
    except ValueError as e:
        # e is the error object; str(e) is its message
        message = str(e)
        number = 0
    assert number == 0
    assert message == "invalid literal for int() with base 10: 'abc'"
    # Print it: print(f"Error found: {e}") inside the except block


def demo_except_clauses() -> None:
    log = []
    for text in ["4", "0", "x"]:
        try:
            value = 8 // int(text)
        except ZeroDivisionError:
            log.append("zero")
        except (ValueError, TypeError) as e:
            log.append(type(e).__name__)
        else:
            log.append(value)  # only when try raised nothing
        finally:
            log.append(".")  # always runs, even after return
    assert log == [2, ".", "zero", ".", "ValueError", "."]


def demo_raise() -> None:
    def withdraw(balance: int, amount: int) -> int:
        if amount > balance:
            raise ValueError(f"cannot withdraw {amount}")
        return balance - amount

    assert withdraw(10, 3) == 7
    message = ""
    try:
        withdraw(10, 50)
    except ValueError as e:
        message = f"Error found: {e}"
    assert message == "Error found: cannot withdraw 50"


def demo_custom_error() -> None:
    message = ""
    try:
        raise CycleError("Cycle detected")
    except ValueError as e:  # also catches every subclass
        message = f"{type(e).__name__}: {e}"
    assert message == "CycleError: Cycle detected"
    assert isinstance(CycleError(), ValueError)


def demo_reraise() -> None:
    prices = {"apple": 3}
    message = ""
    try:
        try:
            prices["pear"] += 1
        except KeyError as e:
            # Translate the error, keeping the original as __cause__
            raise ValueError(f"no price for {e}") from e
    except ValueError as e:
        message = str(e)
    # str() of a KeyError keeps the quotes around the key
    assert message == "no price for 'pear'"
    # A bare `raise` inside except re-raises the same error
