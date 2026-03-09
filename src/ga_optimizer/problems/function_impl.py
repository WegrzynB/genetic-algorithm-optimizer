# function_impl.py
# Implementacje funkcji testowych używanych przez katalog problemów.

import math
from collections.abc import Sequence

def hypersphere(x: Sequence[float]) -> float:
    # Funkcja Hypersphere / Sphere:
    # f(x) = sum(x_i^2) dla i = 1..N
    return sum(value ** 2 for value in x)


def hyperellipsoid(x: Sequence[float]) -> float:
    # f(x) = sum_{i=0}^{N-1} sum_{j=0}^{i} x_j^2
    total = 0.0
    for i in range(len(x)):
        for j in range(i + 1):
            total += x[j] ** 2
    return total


def schwefel(x: Sequence[float]) -> float:
    # f(x) = 418.9829*N - sum(x_i * sin(sqrt(|x_i|)))
    n = len(x)
    total = sum(value * math.sin(math.sqrt(abs(value))) for value in x)
    return 418.9829 * n - total


def ackley(x: Sequence[float], a: float = 20, b: float = 0.2, c: float = 2 * math.pi) -> float:
    n = len(x)

    sum_sq = sum(value ** 2 for value in x)
    sum_cos = sum(math.cos(c * value) for value in x)

    term1 = -a * math.exp(-b * math.sqrt(sum_sq / n))
    term2 = -math.exp(sum_cos / n)

    return term1 + term2 + a + math.e


def michalewicz(x: Sequence[float], m: int = 10) -> float:
    total = 0.0
    for i, value in enumerate(x):
        total += math.sin(value) * (math.sin((i + 1) * value ** 2 / math.pi) ** (2 * m))
    return -total


def rastrigin(x: Sequence[float]) -> float:
    n = len(x)
    return 10 * n + sum(value ** 2 - 10 * math.cos(2 * math.pi * value) for value in x)


def rosenbrock(x: Sequence[float]) -> float:
    total = 0.0
    for i in range(len(x) - 1):
        total += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
    return total


def dejong3(x: Sequence[float]) -> float:
    # f(x) = sum(floor(x_i))
    return sum(math.floor(value) for value in x)


def martin_gaddy(x: Sequence[float]) -> float:
    x1, x2 = x
    return (x1 - x2) ** 2 + ((x1 + x2 - 10) / 3) ** 2
    
def griewank(x: Sequence[float]) -> float:
    sum_term = sum(value ** 2 / 4000.0 for value in x)
    prod_term = 1.0
    for i, value in enumerate(x):
        prod_term *= math.cos(value / math.sqrt(i + 1))
    return sum_term - prod_term + 1

