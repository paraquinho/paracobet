"""Idempotent local seed: `python scripts/seed_mock.py` from apps/api."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.infrastructure.database import SessionLocal
from app.infrastructure.models import (
    Bookmaker,
    Competition,
    Country,
    Market,
    MarketSelection,
    Match,
    MatchStatistic,
    MatchTeam,
    OddsSnapshot,
    Season,
    Sport,
    Team,
    Venue,
)


def one(session, model, **filters):
    return session.scalar(select(model).filter_by(**filters))


def seed() -> None:
    session = SessionLocal()
    try:
        now = datetime.now(UTC)
        sport = one(session, Sport, name="Football") or Sport(name="Football")
        country = one(session, Country, code="ESP") or Country(name="Spain", code="ESP")
        session.add_all([sport, country])
        session.flush()
        competition = one(
            session, Competition, provider="mock", external_id="comp-001"
        ) or Competition(
            provider="mock",
            external_id="comp-001",
            sport_id=sport.id,
            country_id=country.id,
            name="Iberian Analytics League",
        )
        session.add(competition)
        session.flush()
        season = one(session, Season, competition_id=competition.id, name="2025/26") or Season(
            competition_id=competition.id, name="2025/26"
        )
        venue = one(session, Venue, name="Estadio de Datos") or Venue(
            name="Estadio de Datos", city="Madrid", capacity=42000
        )
        session.add_all([season, venue])
        session.flush()
        teams = []
        for external_id, name in (("team-001", "Atlético Norte"), ("team-002", "Costa Azul")):
            team = one(session, Team, provider="mock", external_id=external_id) or Team(
                provider="mock",
                external_id=external_id,
                sport_id=sport.id,
                country_id=country.id,
                name=name,
            )
            teams.append(team)
            session.add(team)
        session.flush()
        match = one(session, Match, provider="mock", external_id="match-001") or Match(
            provider="mock",
            external_id="match-001",
            competition_id=competition.id,
            season_id=season.id,
            venue_id=venue.id,
            status="scheduled",
            starts_at=now + timedelta(hours=3),
            source="mock",
            available_at=now,
        )
        session.add(match)
        session.flush()
        for team, side in zip(teams, ("home", "away"), strict=True):
            if not one(session, MatchTeam, match_id=match.id, team_id=team.id):
                session.add(MatchTeam(match_id=match.id, team_id=team.id, side=side))
        if not one(
            session, MatchStatistic, match_id=match.id, metric="corners", team_id=teams[0].id
        ):
            session.add(
                MatchStatistic(
                    match_id=match.id,
                    team_id=teams[0].id,
                    metric="corners",
                    value=5.8,
                    event_time=match.starts_at,
                    available_at=now,
                    source="mock",
                )
            )
        bookmaker = one(session, Bookmaker, name="MockBook") or Bookmaker(
            name="MockBook", provider="mock", external_id="bookmaker-001"
        )
        market = one(session, Market, key="total_goals") or Market(
            sport_id=sport.id,
            key="total_goals",
            name="Total goals",
            provider="mock",
            external_id="market-001",
        )
        session.add_all([bookmaker, market])
        session.flush()
        selection = one(
            session, MarketSelection, market_id=market.id, name="Over 2.5"
        ) or MarketSelection(
            market_id=market.id,
            name="Over 2.5",
            line=2.5,
            provider="mock",
            external_id="selection-001",
        )
        session.add(selection)
        session.flush()
        captured = datetime(2026, 1, 1, tzinfo=UTC)
        if not one(
            session,
            OddsSnapshot,
            match_id=match.id,
            selection_id=selection.id,
            bookmaker_id=bookmaker.id,
            observed_at=captured,
        ):
            session.add(
                OddsSnapshot(
                    match_id=match.id,
                    selection_id=selection.id,
                    bookmaker_id=bookmaker.id,
                    decimal_odds=1.82,
                    observed_at=captured,
                    available_at=captured,
                    source="mock",
                    is_available=True,
                )
            )
        session.commit()
        print("Mock seed complete: competition, teams, match, statistics, market and odds snapshot")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
