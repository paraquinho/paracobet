from fastapi import APIRouter, Depends, HTTPException, Query

from app.analytics.historical import historical_window
from app.api.dependencies import get_match_service
from app.domain.entities import MatchDetail, MatchSummary
from app.services.matches import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchSummary])
def list_matches(
    status: str | None = Query(default=None),
    competition: str | None = Query(default=None),
    service: MatchService = Depends(get_match_service),
) -> list[MatchSummary]:
    return service.list_matches(status, competition)


@router.get("/{match_id}/history")
def match_history(
    match_id: str,
    metric: str = "goals",
    window: int = 5,
    venue: str = "all",
    line: float | None = None,
    service: MatchService = Depends(get_match_service),
) -> dict[str, object]:
    match = service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    values = (
        match.recent_form["home" if venue == "home" else "away"]
        if venue in {"home", "away"}
        else match.recent_form["home"] + match.recent_form["away"]
    )
    return {
        "match_id": match_id,
        "metric": metric,
        **historical_window(values, window, venue, line),
    }


@router.get("/{match_id}", response_model=MatchDetail)
def get_match(match_id: str, service: MatchService = Depends(get_match_service)) -> MatchDetail:
    match = service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
