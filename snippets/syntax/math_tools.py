import math


def demo_math() -> None:
    assert math.gcd(12, 18) == 6
    assert math.lcm(4, 6) == 12
    assert math.isqrt(17) == 4
    assert math.sqrt(16) == 4.0
    assert math.ceil(7 / 2) == 4
    assert math.floor(7 / 2) == 3
    assert math.log2(8) == 3.0
    assert math.log10(1000) == 3.0
    assert math.prod([2, 3, 4]) == 24
    assert math.factorial(5) == 120


def demo_combinatorics() -> None:
    # Choose 2 of 5 (order ignored) and arrange 2 of 5 (order matters)
    assert math.comb(5, 2) == 10
    assert math.perm(5, 2) == 20
    assert math.dist((0, 0), (3, 4)) == 5.0
    assert math.hypot(3, 4) == 5.0


def demo_integer_division() -> None:
    assert 7 // 2 == 3
    # // floors toward negative infinity
    assert -7 // 2 == -4
    assert int(-7 / 2) == -3
    # % takes the sign of the divisor
    assert -7 % 2 == 1
    assert divmod(-7, 2) == (-4, 1)
    # Ceiling division without floats
    assert -(-7 // 2) == 4
    modulus = 10**9 + 7
    assert (modulus + 5) % modulus == 5
