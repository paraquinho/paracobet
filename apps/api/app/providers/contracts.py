"""Stable provider contracts and normalized transport records.

Adapters return these records; domain and persistence code never imports a vendor SDK.
"""

from datetime import datetime
from typing import Protocol

from pydantic import BaseModel, Field


class ExternalRef(BaseModel):
    provider: str = Field(min_length=1)
    external_id: str = Field(min_length=1)


class ProviderCompetition(BaseModel):
    ref: ExternalRef
    name: str
    country: str | None = None
    sport: str = "football"


class ProviderTeam(BaseModel):
    ref: ExternalRef
    name: str
    sport: str = "football"
    country: str | None = None


class ProviderPlayer(BaseModel):
    ref: ExternalRef
    name: str
    team_ref: ExternalRef | None = None
    position: str | None = None


class ProviderMatch(BaseModel):
    ref: ExternalRef
    competition_ref: ExternalRef
    home_team_ref: ExternalRef
    away_team_ref: ExternalRef
    starts_at: datetime
    status: str
    venue: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    event_time: datetime | None = None
    available_at: datetime


class ProviderStatistic(BaseModel):
    match_ref: ExternalRef
    metric: str
    value: float
    team_ref: ExternalRef | None = None
    player_ref: ExternalRef | None = None
    event_time: datetime | None = None
    available_at: datetime


class ProviderBookmaker(BaseModel):
    ref: ExternalRef
    name: str


class ProviderMarketSelection(BaseModel):
    ref: ExternalRef
    market_ref: ExternalRef
    match_ref: ExternalRef
    bookmaker_ref: ExternalRef
    market: str
    selection: str
    line: float | None = None
    odds: float = Field(gt=1)
    captured_at: datetime
    available_at: datetime


class SportsProvider(Protocol):
    def competitions(self) -> list[ProviderCompetition]: ...
    def seasons(self) -> list[dict[str, object]]: ...
    def teams(self) -> list[ProviderTeam]: ...
    def players(self) -> list[ProviderPlayer]: ...
    def matches(self) -> list[ProviderMatch]: ...
    def match_statistics(self) -> list[ProviderStatistic]: ...
    def player_statistics(self) -> list[ProviderStatistic]: ...


class OddsProvider(Protocol):
    def bookmakers(self) -> list[ProviderBookmaker]: ...
    def selections(self) -> list[ProviderMarketSelection]: ...
