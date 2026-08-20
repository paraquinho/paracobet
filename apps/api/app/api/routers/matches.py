from fastapi import APIRouter, Depends, HTTPException, Query

from app.analytics.historical import historical_window
from app.api.dependencies import get_match_service
from app.domain.entities import MatchDetail, MatchSummary, TeamForm, TeamStatistics
from app.services.matches import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])

teams_router = APIRouter(prefix="/teams", tags=["teams"])


@teams_router.get("/{team_id}/statistics", response_model=TeamStatistics)
def team_statistics(team_id: int, competition_id: int = Query(..., alias="competition"), season: int = Query(...), service: MatchService = Depends(get_match_service)) -> TeamStatistics:
    return service.team_statistics(team_id, competition_id, season)


@teams_router.get("/{team_id}/form", response_model=TeamForm)
def team_form(team_id: int, competition_id: int = Query(..., alias="competition"), season: int = Query(...), service: MatchService = Depends(get_match_service)) -> TeamForm:
    return service.team_form(team_id, competition_id, season)


@router.get("", response_model=list[MatchSummary])
def list_matches(
    status: str | None = Query(default=None),
    competition: str | None = Query(default=None),
    date: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    timezone: str = Query(default="America/Bogota"),
    service: MatchService = Depends(get_match_service),
) -> list[MatchSummary]:
    return service.list_matches(status, competition, date, timezone)


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
