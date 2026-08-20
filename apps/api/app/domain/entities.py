from datetime import datetime

from pydantic import BaseModel, Field


class MatchSummary(BaseModel):
    id: str
    sport: str = "football"
    competition: str
    country: str
    home_team: str
    away_team: str
    starts_at: datetime
    status: str
    score: str | None = None
    source: str = "mock"
    home_team_id: int | None = None
    away_team_id: int | None = None
    home_logo: str | None = None
    away_logo: str | None = None
    season: int | None = None
    round: str | None = None
    competition_id: int | None = None


class MatchDetail(MatchSummary):
    venue: str
    statistics: dict[str, dict[str, float]]
    recent_form: dict[str, list[float]]
    markets: list["MarketQuote"]


class MarketQuote(BaseModel):
    id: str
    match_id: str
    market: str
    selection: str
    line: float | None = None
    odds: float = Field(gt=1)
    bookmaker: str
    observed_at: datetime
    source: str = "mock"


class CompetitionSummary(BaseModel):
    id: str
    name: str
    country: str
    sport: str = "football"
