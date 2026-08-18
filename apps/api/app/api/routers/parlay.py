from fastapi import APIRouter

from app.schemas.parlay import ParlayAnalyzeRequest, ParlayAnalyzeResponse, analyze_parlay

router = APIRouter(prefix="/parlay", tags=["parlay"])


@router.post("/analyze", response_model=ParlayAnalyzeResponse)
def analyze(payload: ParlayAnalyzeRequest) -> ParlayAnalyzeResponse:
    return analyze_parlay(payload)


@router.post("/build")
def build() -> dict[str, str]:
    return {"status": "planned", "detail": "Candidate generation is prepared for the next phase."}
