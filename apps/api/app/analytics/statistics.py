from collections.abc import Sequence
from math import prod

import numpy as np


def historical_summary(
    values: Sequence[float], line: float | None = None
) -> dict[str, float | list[float]]:
    if not values:
        raise ValueError("At least one historical value is required")
    series = np.array(values, dtype=float)
    result: dict[str, float | list[float]] = {
        "average": float(np.mean(series)),
        "median": float(np.median(series)),
        "minimum": float(np.min(series)),
        "maximum": float(np.max(series)),
        "standard_deviation": float(np.std(series)),
        "distribution": series.tolist(),
    }
    if line is not None:
        result["over_frequency"] = float(np.mean(series > line))
        result["under_frequency"] = float(np.mean(series < line))
    return result


def implied_probability(decimal_odds: float) -> float:
    if decimal_odds <= 1:
        raise ValueError("Decimal odds must be greater than 1")
    return 1 / decimal_odds


def edge(model_probability: float, decimal_odds: float) -> float:
    return model_probability - implied_probability(decimal_odds)


def expected_value(model_probability: float, decimal_odds: float) -> float:
    return (model_probability * decimal_odds) - 1


def combined_independent_probability(probabilities: Sequence[float]) -> float:
    if not probabilities or any(p < 0 or p > 1 for p in probabilities):
        raise ValueError("Probabilities must be a non-empty sequence between 0 and 1")
    return float(prod(probabilities))
