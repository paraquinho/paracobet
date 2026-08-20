"""API-Football adapter. Vendor payloads stop at this boundary."""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.core.config import settings
from app.domain.entities import CompetitionSummary, MarketQuote, MatchDetail, MatchSummary
from app.providers.base import SportsDataProvider


class ApiFootballError(RuntimeError):
    """A safe, non-sensitive provider failure that can trigger mock fallback."""


class ApiFootballProvider(SportsDataProvider):
    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], tuple[float, list[MatchSummary]]] = {}
        self._matches: dict[str, MatchSummary] = {}
        self._lock = threading.Lock()

    def list_matches(self, date: str | None = None, timezone: str = "America/Bogota") -> list[MatchSummary]:
        if not settings.api_football_key:
            raise ApiFootballError("API key unavailable")
        requested_date = date or self._today_in_timezone(timezone)
        cache_key = (requested_date, timezone)
        now = time.monotonic()
        with self._lock:
            cached = self._cache.get(cache_key)
            if cached and now - cached[0] < settings.api_football_cache_seconds:
                return cached[1]
        payload = self._request("fixtures", {"date": requested_date, "timezone": timezone})
        errors = payload.get("errors")
        if isinstance(errors, dict) and errors:
            raise ApiFootballError("Provider returned an error")
        fixtures = payload.get("response")
        if not isinstance(fixtures, list):
            raise ApiFootballError("Invalid fixtures response")
        matches = [self._normalize(item) for item in fixtures if isinstance(item, dict)]
        with self._lock:
            self._cache[cache_key] = (now, matches)
            self._matches.update({match.id: match for match in matches})
        return matches

    def get_match(self, match_id: str) -> MatchDetail | None:
        match = self._matches.get(match_id)
        if not match:
            return None
        return MatchDetail(**match.model_dump(), venue="API-Football", statistics={}, recent_form={}, markets=[])

    def list_competitions(self) -> list[CompetitionSummary]:
        return []

    def list_markets(self, match_id: str | None = None) -> list[MarketQuote]:
        return []

    def _request(self, resource: str, params: dict[str, str]) -> dict[str, object]:
        url = f"{settings.api_football_base_url.rstrip('/')}/{resource}?{urlencode(params)}"
        request = Request(url, headers={"x-apisports-key": settings.api_football_key or ""}, method="GET")
        try:
            with urlopen(request, timeout=settings.api_football_timeout_seconds) as response:
                if response.status != 200:
                    raise ApiFootballError(f"Provider HTTP {response.status}")
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code in {401, 403, 429}:
                raise ApiFootballError(f"Provider HTTP {exc.code}") from exc
            raise ApiFootballError("Provider HTTP error") from exc
        except (TimeoutError, URLError, OSError, json.JSONDecodeError) as exc:
            raise ApiFootballError("Provider request failed") from exc
        if not isinstance(data, dict):
            raise ApiFootballError("Invalid provider payload")
        return data

    @staticmethod
    def _today_in_timezone(timezone: str) -> str:
        try:
            return datetime.now(ZoneInfo(timezone)).date().isoformat()
        except ZoneInfoNotFoundError as exc:
            raise ApiFootballError("Invalid timezone") from exc

    @staticmethod
    def _normalize(item: dict[str, object]) -> MatchSummary:
        fixture = item.get("fixture") if isinstance(item.get("fixture"), dict) else {}
        teams = item.get("teams") if isinstance(item.get("teams"), dict) else {}
        home = teams.get("home") if isinstance(teams.get("home"), dict) else {}
        away = teams.get("away") if isinstance(teams.get("away"), dict) else {}
        league = item.get("league") if isinstance(item.get("league"), dict) else {}
        goals = item.get("goals") if isinstance(item.get("goals"), dict) else {}
        fixture_id = fixture.get("id")
        starts_at = fixture.get("date")
        if not fixture_id or not isinstance(starts_at, str):
            raise ApiFootballError("Invalid fixture record")
        status_data = fixture.get("status") if isinstance(fixture.get("status"), dict) else {}
        status_short = str(status_data.get("short") or "NS")
        status = "finished" if status_short in {"FT", "AET", "PEN"} else "scheduled"
        home_name = str(home.get("name") or "Equipo local")
        away_name = str(away.get("name") or "Equipo visitante")
        home_goals, away_goals = goals.get("home"), goals.get("away")
        score = None if home_goals is None or away_goals is None else f"{home_goals} - {away_goals}"
        return MatchSummary(id=f"af-{fixture_id}", competition=str(league.get("name") or "Fútbol"), country=str(league.get("country") or ""), home_team=home_name, away_team=away_name, starts_at=datetime.fromisoformat(starts_at.replace("Z", "+00:00")), status=status, score=score, source="api-football", home_team_id=home.get("id") if isinstance(home.get("id"), int) else None, away_team_id=away.get("id") if isinstance(away.get("id"), int) else None, home_logo=home.get("logo") if isinstance(home.get("logo"), str) else None, away_logo=away.get("logo") if isinstance(away.get("logo"), str) else None, season=league.get("season") if isinstance(league.get("season"), int) else None, round=league.get("round") if isinstance(league.get("round"), str) else None, competition_id=league.get("id") if isinstance(league.get("id"), int) else None)
