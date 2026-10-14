import sys
from decimal import Decimal, localcontext


def valid_input(data: str) -> bool:
    tokens = data.split()
    try:
        values = [int(token) for token in tokens]
    except ValueError:
        return False
    if len(values) < 2:
        return False
    n, payload = values[0], values[1]
    if not 2 <= n <= 1000 or not 1 <= payload <= 1000:
        return False
    if len(values) != 2 + 2 * n:
        return False
    coefficients = values[2:]
    if any(value < 1 or value > 1000 for value in coefficients):
        return False
    if any(value == 1 for value in coefficients):
        return True

    with localcontext() as context:
        context.prec = 80
        total_mass = Decimal(payload)
        payload_mass = Decimal(payload)
        maximum_fuel = Decimal(10**9)
        for coefficient in coefficients:
            factor = Decimal(coefficient) / Decimal(coefficient - 1)
            total_mass *= factor
            if total_mass - payload_mass > maximum_fuel:
                return False
    return True


if __name__ == "__main__":
    raise SystemExit(0 if valid_input(sys.stdin.read()) else 1)
