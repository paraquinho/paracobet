"""SQLAlchemy persistence models; snapshots are append-only by domain rule."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class IdentifiedModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Sport(IdentifiedModel):
    __tablename__ = "sports"
    name: Mapped[str] = mapped_column(String(80), unique=True)


class Country(IdentifiedModel):
    __tablename__ = "countries"
    name: Mapped[str] = mapped_column(String(120))
    code: Mapped[str] = mapped_column(String(3), unique=True)


class Competition(IdentifiedModel):
    __tablename__ = "competitions"
    sport_id: Mapped[UUID] = mapped_column(ForeignKey("sports.id"))
    country_id: Mapped[UUID | None] = mapped_column(ForeignKey("countries.id"))
    name: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))
    __table_args__ = (
        UniqueConstraint("provider", "external_id", name="uq_competition_provider_external"),
    )


class Season(IdentifiedModel):
    __tablename__ = "seasons"
    competition_id: Mapped[UUID] = mapped_column(ForeignKey("competitions.id"))
    name: Mapped[str] = mapped_column(String(40))


class Team(IdentifiedModel):
    __tablename__ = "teams"
    sport_id: Mapped[UUID] = mapped_column(ForeignKey("sports.id"))
    country_id: Mapped[UUID | None] = mapped_column(ForeignKey("countries.id"))
    name: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))
    __table_args__ = (
        UniqueConstraint("provider", "external_id", name="uq_team_provider_external"),
    )


class Player(IdentifiedModel):
    __tablename__ = "players"
    team_id: Mapped[UUID | None] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String(160))
    position: Mapped[str | None] = mapped_column(String(40))


class Venue(IdentifiedModel):
    __tablename__ = "venues"
    name: Mapped[str] = mapped_column(String(160))
    city: Mapped[str | None] = mapped_column(String(120))
    capacity: Mapped[int | None] = mapped_column(Integer)


class Match(IdentifiedModel):
    __tablename__ = "matches"
    competition_id: Mapped[UUID] = mapped_column(ForeignKey("competitions.id"))
    season_id: Mapped[UUID | None] = mapped_column(ForeignKey("seasons.id"))
    venue_id: Mapped[UUID | None] = mapped_column(ForeignKey("venues.id"))
    status: Mapped[str] = mapped_column(String(32))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(40))
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))
    available_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("provider", "external_id", name="uq_match_provider_external"),
    )


class MatchTeam(Base):
    __tablename__ = "match_teams"
    match_id: Mapped[UUID] = mapped_column(ForeignKey("matches.id"), primary_key=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    side: Mapped[str] = mapped_column(String(8))
    score: Mapped[int | None] = mapped_column(Integer)


class MatchStatistic(IdentifiedModel):
    __tablename__ = "match_statistics"
    match_id: Mapped[UUID] = mapped_column(ForeignKey("matches.id"))
    team_id: Mapped[UUID | None] = mapped_column(ForeignKey("teams.id"))
    metric: Mapped[str] = mapped_column(String(80))
    value: Mapped[float] = mapped_column(Float)
    event_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    available_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(40))


class PlayerStatistic(IdentifiedModel):
    __tablename__ = "player_statistics"
    match_id: Mapped[UUID] = mapped_column(ForeignKey("matches.id"))
    player_id: Mapped[UUID] = mapped_column(ForeignKey("players.id"))
    metric: Mapped[str] = mapped_column(String(80))
    value: Mapped[float] = mapped_column(Float)


class Bookmaker(IdentifiedModel):
    __tablename__ = "bookmakers"
    name: Mapped[str] = mapped_column(String(120), unique=True)
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))


class DataProvider(IdentifiedModel):
    __tablename__ = "data_providers"
    name: Mapped[str] = mapped_column(String(120), unique=True)
    is_mock: Mapped[bool] = mapped_column(Boolean, default=False)


class Market(IdentifiedModel):
    __tablename__ = "markets"
    sport_id: Mapped[UUID] = mapped_column(ForeignKey("sports.id"))
    key: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))


class MarketSelection(IdentifiedModel):
    __tablename__ = "market_selections"
    market_id: Mapped[UUID] = mapped_column(ForeignKey("markets.id"))
    name: Mapped[str] = mapped_column(String(160))
    line: Mapped[float | None] = mapped_column(Float)
    provider: Mapped[str] = mapped_column(String(80), default="internal")
    external_id: Mapped[str | None] = mapped_column(String(160))


class OddsSnapshot(IdentifiedModel):
    __tablename__ = "odds_snapshots"
    match_id: Mapped[UUID] = mapped_column(ForeignKey("matches.id"))
    selection_id: Mapped[UUID] = mapped_column(ForeignKey("market_selections.id"))
    bookmaker_id: Mapped[UUID] = mapped_column(ForeignKey("bookmakers.id"))
    decimal_odds: Mapped[float] = mapped_column(Float)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(40))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
