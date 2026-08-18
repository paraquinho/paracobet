from datetime import UTC, datetime, timedelta

from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary
from app.providers.base import SportsDataProvider


class MockDataProvider(SportsDataProvider):
    """Synthetic development-only data. It must never be labelled as production data."""

    def __init__(self) -> None:
        now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
        self._matches = [
            MatchSummary(
                id="mock-001",
                competition="Iberian Analytics League",
                country="Spain",
                home_team="Atlético Norte",
                away_team="Costa Azul",
                starts_at=now + timedelta(hours=3),
                status="scheduled",
            ),
            MatchSummary(
                id="mock-002",
                competition="Iberian Analytics League",
                country="Spain",
                home_team="Real Montaña",
                away_team="Deportivo Río",
                starts_at=now + timedelta(hours=5),
                status="scheduled",
            ),
            MatchSummary(
                id="mock-003",
                competition="Premier Metrics",
                country="England",
                home_team="West Harbour",
                away_team="Kingsbridge",
                starts_at=now - timedelta(hours=2),
                status="finished",
                score="2 - 1",
            ),
            MatchSummary(
                id="mock-004",
                competition="Premier Metrics",
                country="England",
                home_team="Northbridge",
                away_team="Elm City",
                starts_at=now - timedelta(days=1),
                status="finished",
                score="1 - 1",
            ),
        ]
        self._markets = [
            MarketQuote(
                id="q-001",
                match_id="mock-001",
                market="Total goals",
                selection="Over 2.5",
                line=2.5,
                odds=1.82,
                bookmaker="MockBook",
                observed_at=now,
                source="mock",
            ),
            MarketQuote(
                id="q-002",
                match_id="mock-001",
                market="Total corners",
                selection="Over 8.5",
                line=8.5,
                odds=1.91,
                bookmaker="MockBook",
                observed_at=now,
                source="mock",
            ),
            MarketQuote(
                id="q-003",
                match_id="mock-001",
                market="Both teams score",
                selection="Yes",
                odds=1.74,
                bookmaker="MockBook",
                observed_at=now,
                source="mock",
            ),
            MarketQuote(
                id="q-004",
                match_id="mock-002",
                market="Total goals",
                selection="Under 3.5",
                line=3.5,
                odds=1.48,
                bookmaker="MockBook",
                observed_at=now,
                source="mock",
            ),
            MarketQuote(
                id="q-005",
                match_id="mock-003",
                market="Total corners",
                selection="Over 9.5",
                line=9.5,
                odds=2.04,
                bookmaker="MockBook",
                observed_at=now - timedelta(hours=3),
                source="mock",
            ),
        ]

    def list_matches(self) -> list[MatchSummary]:
        return self._matches

    def get_match(self, match_id: str) -> MatchDetail | None:
        match = next((item for item in self._matches if item.id == match_id), None)
        if not match:
            return None
        return MatchDetail(
            **match.model_dump(),
            venue="Estadio de Datos",
            markets=self.list_markets(match_id),
            statistics={
                "goals": {"home": 1.6, "away": 1.2},
                "shots": {"home": 13.4, "away": 10.8},
                "shots_on_target": {"home": 5.1, "away": 4.2},
                "corners": {"home": 5.8, "away": 4.9},
                "cards": {"home": 2.1, "away": 2.5},
                "fouls": {"home": 11.2, "away": 12.7},
                "possession": {"home": 53.0, "away": 47.0},
            },
            recent_form={"home": [2.0, 1.0, 3.0, 1.0, 2.0], "away": [1.0, 2.0, 0.0, 2.0, 1.0]},
        )

    def list_competitions(self) -> list[CompetitionSummary]:
        return [
            CompetitionSummary(id="comp-001", name="Iberian Analytics League", country="Spain"),
            CompetitionSummary(id="comp-002", name="Premier Metrics", country="England"),
        ]

    def list_markets(self, match_id: str | None = None) -> list[MarketQuote]:
        return [quote for quote in self._markets if match_id is None or quote.match_id == match_id]
