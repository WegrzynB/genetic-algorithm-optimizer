# function_impl.py
# Implementacje funkcji testowych używanych przez katalog problemów.

from collections.abc import Sequence


def hypersphere(x: Sequence[float]) -> float:
    # Funkcja Hypersphere / Sphere:
    # f(x) = sum(x_i^2) dla i = 1..N
    return sum(value ** 2 for value in x)