from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary
from app.providers.base import SportsDataProvider


class MatchService:
    def __init__(self, provider: SportsDataProvider, repository=None) -> None:
        self.provider = provider
        self.repository = repository

    def list_matches(
        self, status: str | None = None, competition: str | None = None
    ) -> list[MatchSummary]:
        try:
            matches = (
                self.repository.list_summaries()
                if self.repository
                else self.provider.list_matches()
            )
        except Exception:
            if self.repository:
                raise
            # Development remains usable when PostgreSQL is not configured.
            matches = self.provider.list_matches()
        if status:
            matches = [match for match in matches if match.status == status]
        if competition:
            matches = [
                match for match in matches if competition.lower() in match.competition.lower()
            ]
        return matches

    def get_match(self, match_id: str) -> MatchDetail | None:
        return self.provider.get_match(match_id)

    def competitions(self) -> list[CompetitionSummary]:
        return self.provider.list_competitions()

    def markets(self, match_id: str | None = None) -> list[MarketQuote]:
        return self.provider.list_markets(match_id)
