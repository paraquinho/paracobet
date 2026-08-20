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
    competition_logo: str | None = None


class MatchDetail(MatchSummary):
    venue: str
    statistics: dict[str, dict[str, float]]
    recent_form: dict[str, list[float]]
    markets: list["MarketQuote"]


class TeamPerformanceStats(BaseModel):
    played: int | None = None
    wins: int | None = None
    draws: int | None = None
    losses: int | None = None
    goals_for: int | None = None
    goals_against: int | None = None
    goals_for_avg: float | None = None
    goals_against_avg: float | None = None
    clean_sheets: int | None = None
    failed_to_score: int | None = None
    metrics: dict[str, float | None] = Field(default_factory=dict)


class TeamStatistics(BaseModel):
    team_id: int
    team_name: str
    logo: str | None = None
    country: str | None = None
    competition_id: int
    season: int
    source: str = "api-football"
    general: TeamPerformanceStats
    home: TeamPerformanceStats
    away: TeamPerformanceStats


class FormMatch(BaseModel):
    fixture_id: int
    date: datetime
    competition_id: int | None = None
    competition: str | None = None
    opponent_id: int | None = None
    opponent: str
    is_home: bool
    result: str
    goals_for: int | None = None
    goals_against: int | None = None


class FormWindow(BaseModel):
    window: int
    sample_size: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    average_goals_for: float
    average_goals_against: float
    points: int
    possible_points: int
    points_percentage: float
    matches: list[FormMatch] = Field(default_factory=list)


class TeamForm(BaseModel):
    team_id: int
    team_name: str
    competition_id: int
    season: int
    source: str = "api-football"
    windows: dict[str, FormWindow]


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
