import pytest

from app.analytics.historical import historical_window
from app.analytics.statistics import edge, historical_summary, implied_probability


def test_implied_probability() -> None:
    assert implied_probability(1.70) == pytest.approx(0.588235)


def test_edge() -> None:
    assert edge(0.64, 1.70) == pytest.approx(0.0517647)


def test_historical_frequency_and_statistics() -> None:
    summary = historical_summary([7, 9, 10, 11, 12], line=8.5)
    assert summary["average"] == pytest.approx(9.8)
    assert summary["over_frequency"] == pytest.approx(0.8)


def test_historical_window_validation() -> None:
    result = historical_window([1, 2, 3, 4, 5, 6], window=5, venue="home", line=3)
    assert result["window"] == 5
    assert result["over_frequency"] == pytest.approx(0.6)
