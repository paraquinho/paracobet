from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.core.config import settings
from app.infrastructure.database import engine

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
        "data_source": "database" if settings.use_database else "mock",
    }


@router.get("/health/db")
def database_health() -> dict[str, str]:
    """Readiness probe that confirms PostgreSQL is reachable without exposing details."""
    try:
        with engine.connect() as connection:
            connection.execute(text("select 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok", "database": "reachable"}
