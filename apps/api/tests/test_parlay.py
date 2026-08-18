import pytest

from app.schemas.parlay import ParlayAnalyzeRequest, ParlaySelectionInput, analyze_parlay


def test_parlay_analysis_marks_independence_assumption() -> None:
    response = analyze_parlay(
        ParlayAnalyzeRequest(
            selections=[
                ParlaySelectionInput(
                    name="Over 2.5 goals",
                    decimal_odds=1.8,
                    model_probability=0.61,
                    historical_frequency=0.6,
                ),
                ParlaySelectionInput(
                    name="Over 8.5 corners",
                    decimal_odds=1.9,
                    model_probability=0.56,
                    historical_frequency=0.55,
                ),
            ]
        )
    )
    assert response.combined_model_probability == pytest.approx(0.3416)
    assert "Independence" in response.assumption
