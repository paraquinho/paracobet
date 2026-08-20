from abc import ABC, abstractmethod

from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary


class SportsDataProvider(ABC):
    """External data boundary. Implementations normalize provider payloads here."""

    @abstractmethod
    def list_matches(self, date: str | None = None, timezone: str = "America/Bogota") -> list[MatchSummary]: ...

    @abstractmethod
    def get_match(self, match_id: str) -> MatchDetail | None: ...

    @abstractmethod
    def list_competitions(self) -> list[CompetitionSummary]: ...

    @abstractmethod
    def list_markets(self, match_id: str | None = None) -> list[MarketQuote]: ...
