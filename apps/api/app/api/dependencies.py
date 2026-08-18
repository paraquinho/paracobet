from functools import lru_cache

from app.core.config import settings
from app.infrastructure.database import SessionLocal
from app.providers.mock import MockDataProvider
from app.repositories.matches import MatchRepository
from app.services.matches import MatchService


@lru_cache
def get_match_service() -> MatchService:
    repository = MatchRepository(SessionLocal) if settings.use_database else None
    return MatchService(MockDataProvider(), repository)
