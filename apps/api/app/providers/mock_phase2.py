"""Mock adapter implementing both Phase 2 provider contracts."""

from datetime import UTC, datetime, timedelta

from app.providers.contracts import (
    ExternalRef,
    OddsProvider,
    ProviderBookmaker,
    ProviderCompetition,
    ProviderMarketSelection,
    ProviderMatch,
    ProviderPlayer,
    ProviderStatistic,
    ProviderTeam,
    SportsProvider,
)


class MockPhase2Provider(SportsProvider, OddsProvider):
    name = "mock"

    def __init__(self) -> None:
        self.now = datetime.now(UTC)

    def competitions(self) -> list[ProviderCompetition]:
        return [
            ProviderCompetition(
                ref=ExternalRef(provider=self.name, external_id="comp-001"),
                name="Iberian Analytics League",
                country="Spain",
            )
        ]

    def seasons(self) -> list[dict[str, object]]:
        return [
            {
                "provider": self.name,
                "external_id": "season-2025",
                "competition_external_id": "comp-001",
                "name": "2025/26",
            }
        ]

    def teams(self) -> list[ProviderTeam]:
        return [
            ProviderTeam(
                ref=ExternalRef(provider=self.name, external_id="team-001"),
                name="Atlético Norte",
                country="Spain",
            ),
            ProviderTeam(
                ref=ExternalRef(provider=self.name, external_id="team-002"),
                name="Costa Azul",
                country="Spain",
            ),
        ]

    def players(self) -> list[ProviderPlayer]:
        return [
            ProviderPlayer(
                ref=ExternalRef(provider=self.name, external_id="player-001"),
                name="L. Navarro",
                team_ref=ExternalRef(provider=self.name, external_id="team-001"),
                position="FW",
            )
        ]

    def matches(self) -> list[ProviderMatch]:
        return [
            ProviderMatch(
                ref=ExternalRef(provider=self.name, external_id="match-001"),
                competition_ref=ExternalRef(provider=self.name, external_id="comp-001"),
                home_team_ref=ExternalRef(provider=self.name, external_id="team-001"),
                away_team_ref=ExternalRef(provider=self.name, external_id="team-002"),
                starts_at=self.now + timedelta(hours=3),
                status="scheduled",
                available_at=self.now,
            )
        ]

    def match_statistics(self) -> list[ProviderStatistic]:
        match = ExternalRef(provider=self.name, external_id="match-001")
        team = ExternalRef(provider=self.name, external_id="team-001")
        return [
            ProviderStatistic(
                match_ref=match, team_ref=team, metric="corners", value=5.8, available_at=self.now
            )
        ]

    def player_statistics(self) -> list[ProviderStatistic]:
        return []

    def bookmakers(self) -> list[ProviderBookmaker]:
        return [
            ProviderBookmaker(
                ref=ExternalRef(provider=self.name, external_id="bookmaker-001"), name="MockBook"
            )
        ]

    def selections(self) -> list[ProviderMarketSelection]:
        return [
            ProviderMarketSelection(
                ref=ExternalRef(provider=self.name, external_id="selection-001"),
                market_ref=ExternalRef(provider=self.name, external_id="market-001"),
                match_ref=ExternalRef(provider=self.name, external_id="match-001"),
                bookmaker_ref=ExternalRef(provider=self.name, external_id="bookmaker-001"),
                market="Total goals",
                selection="Over 2.5",
                line=2.5,
                odds=1.82,
                captured_at=self.now,
                available_at=self.now,
            )
        ]
