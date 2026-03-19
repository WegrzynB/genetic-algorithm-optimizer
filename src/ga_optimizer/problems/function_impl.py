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


def dejong5(x: Sequence[float]) -> float:
    A = [
        [-32, -16, 0, 16, 32] * 5,
        [-32] * 5 + [-16] * 5 + [0] * 5 + [16] * 5 + [32] * 5,
    ]

    total = 0.002
    for i in range(25):
        denom = i + 1
        denom += (x[0] - A[0][i]) ** 6 + (x[1] - A[1][i]) ** 6
        total += 1.0 / denom

    return 1.0 / total


def easom(x: Sequence[float]) -> float:
    x1, x2 = x
    return -math.cos(x1) * math.cos(x2) * math.exp(-((x1 - math.pi) ** 2 + (x2 - math.pi) ** 2))


def goldstein_price(x: Sequence[float]) -> float:
    x1, x2 = x

    term1 = 1 + (x1 + x2 + 1) ** 2 * (
        19 - 14 * x1 + 3 * x1**2 - 14 * x2 + 6 * x1 * x2 + 3 * x2**2
    )

    term2 = 30 + (2 * x1 - 3 * x2) ** 2 * (
        18 - 32 * x1 + 12 * x1**2 + 48 * x2 - 36 * x1 * x2 + 27 * x2**2
    )

    return term1 * term2


def picheny_goldstein_price(x: Sequence[float]) -> float:
    val = goldstein_price(x)
    return (math.log(val) - 8.693) / 2.427


def styblinski_tang(x: Sequence[float]) -> float:
    return 0.5 * sum(v**4 - 16 * v**2 + 5 * v for v in x)


def mccormick(x: Sequence[float]) -> float:
    x1, x2 = x
    return math.sin(x1 + x2) + (x1 - x2) ** 2 - 1.5 * x1 + 2.5 * x2 + 1


def rana(x: Sequence[float]) -> float:
    total = 0.0
    for i in range(len(x) - 1):
        xi = x[i]
        xj = x[i + 1]

        term1 = xi * math.cos(math.sqrt(abs(xj + xi + 1))) * math.sin(math.sqrt(abs(xj - xi + 1)))
        term2 = (1 + xj) * math.sin(math.sqrt(abs(xj + xi + 1))) * math.cos(math.sqrt(abs(xj - xi + 1)))

        total += term1 + term2

    return total


def eggholder(x: Sequence[float]) -> float:
    total = 0.0
    for i in range(len(x) - 1):
        xi = x[i]
        xj = x[i + 1]

        total += -(xj + 47) * math.sin(math.sqrt(abs(xj + 47 + xi / 2)))
        total += -xi * math.sin(math.sqrt(abs(xi - (xj + 47))))

    return total


def schaffer2(x: Sequence[float]) -> float:
    x1, x2 = x
    num = math.sin(math.sqrt(x1**2 + x2**2)) ** 2 - 0.5
    den = (1 + 0.001 * (x1**2 + x2**2)) ** 2
    return 0.5 + num / den


def himmelblau(x: Sequence[float]) -> float:
    x1, x2 = x
    return (x1**2 + x2 - 11) ** 2 + (x1 + x2**2 - 7) ** 2


def pits_and_holes(x: Sequence[float]) -> float:
    centers = [
        (0, 0), (20, 0), (0, 20), (-20, 0), (0, -20),
        (10, 10), (-10, -10), (-10, 10), (10, -10)
    ]

    values = [0.03, 0.028, 0.026, 0.033, 0.04, 0.08, 0.24, 0.15, 0.21]

    total = 0.0
    for (cx, cy), v in zip(centers, values):
        dx = x[0] - cx
        dy = x[1] - cy
        total -= v * math.exp(-(dx**2 + dy**2) / 50)

    return total
