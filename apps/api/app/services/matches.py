from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary
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
