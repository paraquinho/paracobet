from fastapi import APIRouter, Depends

from app.api.dependencies import get_match_service
from app.domain.entities import CompetitionSummary, MarketQuote
from app.services.matches import MatchService

router = APIRouter(tags=["catalog"])


@router.get("/competitions", response_model=list[CompetitionSummary])
def competitions(service: MatchService = Depends(get_match_service)) -> list[CompetitionSummary]:
    return service.competitions()


@router.get("/teams")
def teams(service: MatchService = Depends(get_match_service)) -> list[dict[str, str]]:
    unique = {
        team for match in service.list_matches() for team in (match.home_team, match.away_team)
    }
    return [
        {"id": f"team-{name.lower().replace(' ', '-')}", "name": name, "source": "mock"}
        for name in sorted(unique)
    ]


@router.get("/markets", response_model=list[MarketQuote])
def markets(
    match_id: str | None = None, service: MatchService = Depends(get_match_service)
) -> list[MarketQuote]:
    return service.markets(match_id)
