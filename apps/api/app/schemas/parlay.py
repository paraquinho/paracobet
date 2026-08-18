from pydantic import BaseModel, Field

from app.analytics.statistics import (
    combined_independent_probability,
    edge,
    expected_value,
    implied_probability,
)

INDEPENDENCE_ASSUMPTION = (
    "Independence approximation only. Selections can be correlated; this is not a guarantee."
)


class ParlaySelectionInput(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    decimal_odds: float = Field(gt=1)
    model_probability: float = Field(ge=0, le=1)
    historical_frequency: float = Field(ge=0, le=1)


class ParlayAnalyzeRequest(BaseModel):
    selections: list[ParlaySelectionInput] = Field(min_length=1, max_length=12)


class SelectionAnalysis(ParlaySelectionInput):
    implied_probability: float
    edge: float
    expected_value: float


class ParlayAnalyzeResponse(BaseModel):
    selections: list[SelectionAnalysis]
    combined_odds: float
    combined_model_probability: float
    combined_implied_probability: float
    expected_value: float
    assumption: str


def analyze_parlay(payload: ParlayAnalyzeRequest) -> ParlayAnalyzeResponse:
    selections = [
        SelectionAnalysis(
            **selection.model_dump(),
            implied_probability=implied_probability(selection.decimal_odds),
            edge=edge(selection.model_probability, selection.decimal_odds),
            expected_value=expected_value(selection.model_probability, selection.decimal_odds),
        )
        for selection in payload.selections
    ]
    combined_odds = 1.0
    for selection in payload.selections:
        combined_odds *= selection.decimal_odds
    probability = combined_independent_probability(
        [item.model_probability for item in payload.selections]
    )
    return ParlayAnalyzeResponse(
        selections=selections,
        combined_odds=round(combined_odds, 3),
        combined_model_probability=probability,
        combined_implied_probability=implied_probability(combined_odds),
        expected_value=expected_value(probability, combined_odds),
        assumption=INDEPENDENCE_ASSUMPTION,
    )
