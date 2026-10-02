import math


def demo_money() -> None:
    amount = 1234.5
    assert f"${amount:,.2f}" == "$1,234.50"
    assert f"${0.5:,.2f}" == "$0.50"
    assert f"${1_000_000:,.2f}" == "$1,000,000.00"
    # Right-align in a column 12 characters wide
    assert f"${amount:>12,.2f}" == "$    1,234.50"


def demo_money_negative() -> None:
    balance = -42.5
    # The sign belongs before the dollar sign
    sign = "-" if balance < 0 else ""
    assert f"{sign}${abs(balance):,.2f}" == "-$42.50"
    assert f"${balance:,.2f}" == "$-42.50"


def demo_cents() -> None:
    # Floats cannot store 0.1 exactly, so keep money in integer cents
    assert 0.1 + 0.2 != 0.3
    assert math.isclose(0.1 + 0.2, 0.3)
    price_cents = 1999
    total_cents = price_cents * 3
    dollars, cents = divmod(total_cents, 100)
    assert f"${dollars:,}.{cents:02d}" == "$59.97"
    assert f"${total_cents / 100:,.2f}" == "$59.97"
    # Parse a price string into cents
    price = "$1,234.56"
    parsed = round(float(price.lstrip("$").replace(",", "")) * 100)
    assert parsed == 123456


def demo_decimals_and_separators() -> None:
    value = 3.14159
    assert f"{value:.2f}" == "3.14"
    assert f"{value:.0f}" == "3"
    assert f"{1234567:,}" == "1,234,567"
    assert f"{1234567:_}" == "1_234_567"
    assert f"{0.256:.1%}" == "25.6%"
    assert f"{12:+d}" == "+12"
    assert f"{1500000:.2e}" == "1.50e+06"


def demo_alignment() -> None:
    name = "ada"
    assert f"{name:<6}|" == "ada   |"
    assert f"{name:>6}|" == "   ada|"
    assert f"{name:^7}|" == "  ada  |"
    assert f"{name:*^7}" == "**ada**"
    assert f"{42:05d}" == "00042"
    width = 8
    assert f"{name:>{width}}" == "     ada"
    assert f"{'item':<6}{'cost':>6}" == "item    cost"
    assert "7".zfill(3) == "007"


def demo_format_bases() -> None:
    assert f"{10:b}" == "1010"
    assert f"{10:08b}" == "00001010"
    assert f"{255:x}" == "ff"
    assert f"{255:#x}" == "0xff"
    assert f"{255:X}" == "FF"
    assert f"{8:o}" == "10"


def demo_debugging() -> None:
    total = 3
    assert f"{total=}" == "total=3"
    assert f"{total = }" == "total = 3"
    assert f"{'hi'!r}" == "'hi'"
    assert f"{{braces}} {total}" == "{braces} 3"


def demo_rounding() -> None:
    # round() rounds half to even ("banker's rounding")
    assert round(2.5) == 2
    assert round(3.5) == 4
    assert round(1234.5678, 2) == 1234.57
    assert round(1234.5678, -2) == 1200.0
    # 2.675 is stored as 2.67499999..., so it rounds down
    assert round(2.675, 2) == 2.67
    # int() truncates toward zero; floor and ceil do not
    assert int(-2.9) == -2
    assert math.floor(-2.9) == -3
    assert math.ceil(2.1) == 3
