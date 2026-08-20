from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary, TeamForm, TeamStatistics
from app.providers.base import SportsDataProvider


class MatchService:
    def __init__(self, provider: SportsDataProvider, repository=None) -> None:
        self.provider = provider
        self.repository = repository
        self.fallback = None

    def with_fallback(self, fallback: SportsDataProvider) -> "MatchService":
        self.fallback = fallback
        return self

    def list_matches(
        self, status: str | None = None, competition: str | None = None, date: str | None = None,
        timezone: str = "America/Bogota",
    ) -> list[MatchSummary]:
        try:
            matches = self.provider.list_matches(date, timezone)
        except Exception:
            if self.fallback:
                matches = self.fallback.list_matches(date, timezone)
            elif self.repository:
                matches = self.repository.list_summaries()
            else:
                raise
        if status:
            matches = [match for match in matches if match.status == status]
        if competition:
            matches = [
                match for match in matches if competition.lower() in match.competition.lower()
            ]
        return matches

    def get_match(self, match_id: str) -> MatchDetail | None:
        match = self.provider.get_match(match_id)
        return match if match else self.fallback.get_match(match_id) if self.fallback else None

    def competitions(self) -> list[CompetitionSummary]:
        result = self.provider.list_competitions()
        return result or self.fallback.list_competitions() if self.fallback else result

    def markets(self, match_id: str | None = None) -> list[MarketQuote]:
        result = self.provider.list_markets(match_id)
        return result or self.fallback.list_markets(match_id) if self.fallback else result

    def team_statistics(self, team_id: int, competition_id: int, season: int) -> TeamStatistics:
        try:
            return self.provider.get_team_statistics(team_id, competition_id, season)  # type: ignore[attr-defined]
        except Exception:
            return TeamStatistics(team_id=team_id, team_name="Datos no disponibles", competition_id=competition_id, season=season, source="mock", general={}, home={}, away={})

    def team_form(self, team_id: int, competition_id: int, season: int) -> TeamForm:
        try:
            return self.provider.get_team_form(team_id, competition_id, season)  # type: ignore[attr-defined]
        except Exception:
            from app.domain.entities import FormWindow
            empty = {f"L{size}": FormWindow(window=size, sample_size=0, wins=0, draws=0, losses=0, goals_for=0, goals_against=0, average_goals_for=0, average_goals_against=0, points=0, possible_points=0, points_percentage=0, matches=[]) for size in (5, 10, 15, 20)}
            return TeamForm(team_id=team_id, team_name="Datos no disponibles", competition_id=competition_id, season=season, source="mock", windows=empty)
