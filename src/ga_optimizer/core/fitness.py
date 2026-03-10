# logika przeliczania wartości funkcji celu na fitness (transformuje jeżeli to konieczne)

def calculate_fitness(raw_objective: float, optimization_type: str = 'min') -> float:
    if optimization_type == 'min':
        # zabezpieczenie przed ujemnymi wartościami fc + odwrócenie skali tzn mniejszy blad to wiekszy fitness
        return 1.0 / (1.0 + abs(raw_objective))
    elif optimization_type == 'max':
        # przy max raw_objective jest już fitness, ale zabezpieczamy przed ujemnymi wartościami
        return max(0.0, raw_objective)
    else:
        raise ValueError(f"Nieobsługiwany typ optymalizacji: {optimization_type}")