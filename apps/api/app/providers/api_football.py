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
from app.domain.entities import (CompetitionSummary, FormMatch, FormWindow, MarketQuote,
                                  MatchDetail, MatchSummary, TeamForm, TeamPerformanceStats,
                                  TeamStatistics)
from app.providers.base import SportsDataProvider


class ApiFootballError(RuntimeError):
    """A safe, non-sensitive provider failure that can trigger mock fallback."""


class ApiFootballProvider(SportsDataProvider):
    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], tuple[float, list[MatchSummary]]] = {}
        self._matches: dict[str, MatchSummary] = {}
        self._team_cache: dict[tuple[str, int, int, int], tuple[float, object]] = {}
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

    def get_team_statistics(self, team_id: int, competition_id: int, season: int) -> TeamStatistics:
        key = ("statistics", team_id, competition_id, season)
        cached = self._cached_team(key)
        if cached:
            return cached
        payload = self._request("teams/statistics", {"team": str(team_id), "league": str(competition_id), "season": str(season)})
        response = payload.get("response")
        if not isinstance(response, dict):
            raise ApiFootballError("Invalid team statistics response")
        team = response.get("team") if isinstance(response.get("team"), dict) else {}
        team_name = team.get("name") if isinstance(team.get("name"), str) and team.get("name") else None
        if not team_name:
            raise ApiFootballError("Team name unavailable")
        stats = TeamStatistics(team_id=team_id, team_name=team_name, logo=team.get("logo") if isinstance(team.get("logo"), str) else None, country=team.get("country") if isinstance(team.get("country"), str) else None, competition_id=competition_id, season=season, general=self._performance(response), home=self._performance(response, "home"), away=self._performance(response, "away"))
        self._store_team(key, stats)
        return stats

    def get_team_form(self, team_id: int, competition_id: int, season: int) -> TeamForm:
        key = ("form", team_id, competition_id, season)
        cached = self._cached_team(key)
        if cached:
            return cached
        payload = self._request("fixtures", {"team": str(team_id), "last": "20", "league": str(competition_id), "season": str(season)})
        response = payload.get("response")
        if not isinstance(response, list):
            raise ApiFootballError("Invalid team form response")
        normalized = [self._normalize_form(item, team_id, competition_id, season) for item in response if isinstance(item, dict)]
        matches = [item for item in normalized if item is not None]
        matches.sort(key=lambda item: item.date, reverse=True)
        windows = {f"L{size}": self._form_window(size, matches[:size]) for size in (5, 10, 15, 20)}
        team_name = next((name for item in response if isinstance(item, dict) for name in self._team_name_candidates(item, team_id)), None)
        if not team_name:
            raise ApiFootballError("Team name unavailable in form response")
        form = TeamForm(team_id=team_id, team_name=team_name, competition_id=competition_id, season=season, windows=windows)
        self._store_team(key, form)
        return form

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

    def _cached_team(self, key: tuple[str, int, int, int]):
        with self._lock:
            cached = self._team_cache.get(key)
        if cached and time.monotonic() - cached[0] < (settings.api_football_cache_seconds * (60 if key[0] == "statistics" else 5)):
            return cached[1]
        return None

    def _store_team(self, key: tuple[str, int, int, int], value: object) -> None:
        with self._lock:
            self._team_cache[key] = (time.monotonic(), value)

    @staticmethod
    def _performance(data: object, side: str | None = None) -> TeamPerformanceStats:
        data = data if isinstance(data, dict) else {}
        fixtures = data.get("fixtures") if isinstance(data.get("fixtures"), dict) else {}
        if side and isinstance(fixtures.get(side), dict):
            fixtures = fixtures[side]
        goals = data.get("goals") if isinstance(data.get("goals"), dict) else {}
        for_goals = goals.get("for") if isinstance(goals.get("for"), dict) else {}
        against_goals = goals.get("against") if isinstance(goals.get("against"), dict) else {}
        def value(obj: object, key: str):
            raw = obj.get(key) if isinstance(obj, dict) else None
            if isinstance(raw, dict): raw = raw.get(side or "total")
            return raw if isinstance(raw, (int, float)) else None
        played = value(fixtures, "played")
        def average(obj: object):
            raw = obj.get("average") if isinstance(obj, dict) else None
            if isinstance(raw, dict): raw = raw.get(side or "total")
            return float(raw) if isinstance(raw, (int, float)) else None
        return TeamPerformanceStats(played=played, wins=value(fixtures, "wins"), draws=value(fixtures, "draws"), losses=value(fixtures, "loses") or value(fixtures, "losses"), goals_for=value(for_goals, "total"), goals_against=value(against_goals, "total"), goals_for_avg=average(for_goals), goals_against_avg=average(against_goals), clean_sheets=value(data.get("clean_sheet"), "total"), failed_to_score=value(data.get("failed_to_score"), "total"), metrics={})

    @staticmethod
    def _normalize_form(item: dict[str, object], team_id: int, competition_id: int, season: int) -> FormMatch | None:
        fixture = item.get("fixture") if isinstance(item.get("fixture"), dict) else {}
        teams = item.get("teams") if isinstance(item.get("teams"), dict) else {}
        home = teams.get("home") if isinstance(teams.get("home"), dict) else {}
        away = teams.get("away") if isinstance(teams.get("away"), dict) else {}
        goals = item.get("goals") if isinstance(item.get("goals"), dict) else {}
        is_home = home.get("id") == team_id
        own, opp = (home, away) if is_home else (away, home)
        own_goals, opp_goals = goals.get("home" if is_home else "away"), goals.get("away" if is_home else "home")
        result = "W" if isinstance(own_goals, int) and isinstance(opp_goals, int) and own_goals > opp_goals else "L" if isinstance(own_goals, int) and isinstance(opp_goals, int) and own_goals < opp_goals else "D"
        league = item.get("league") if isinstance(item.get("league"), dict) else {}
        fixture_id = fixture.get("id")
        league_id = league.get("id")
        league_season = league.get("season")
        if not isinstance(fixture_id, int) or fixture_id <= 0 or (isinstance(league_id, int) and league_id != competition_id) or (isinstance(league_season, int) and league_season != season):
            return None
        starts_at = fixture.get("date")
        if not isinstance(starts_at, str) or not isinstance(home.get("id"), int) or not isinstance(away.get("id"), int) or team_id not in {home["id"], away["id"]}:
            return None
        return FormMatch(fixture_id=fixture_id, date=datetime.fromisoformat(starts_at.replace("Z", "+00:00")), competition_id=league_id if isinstance(league_id, int) else None, competition=league.get("name") if isinstance(league.get("name"), str) else None, opponent_id=opp.get("id") if isinstance(opp.get("id"), int) else None, opponent=str(opp.get("name") or "Rival"), is_home=is_home, result=result, goals_for=own_goals if isinstance(own_goals, int) else None, goals_against=opp_goals if isinstance(opp_goals, int) else None)

    @staticmethod
    def _team_name_candidates(item: dict[str, object], team_id: int) -> list[str]:
        teams = item.get("teams") if isinstance(item.get("teams"), dict) else {}
        names: list[str] = []
        for side in ("home", "away"):
            team = teams.get(side) if isinstance(teams.get(side), dict) else {}
            if team.get("id") == team_id and isinstance(team.get("name"), str) and team["name"]:
                names.append(team["name"])
        return names

    @staticmethod
    def _form_window(size: int, matches: list[FormMatch]) -> FormWindow:
        wins = sum(item.result == "W" for item in matches); draws = sum(item.result == "D" for item in matches); losses = sum(item.result == "L" for item in matches)
        gf = sum(item.goals_for or 0 for item in matches); ga = sum(item.goals_against or 0 for item in matches); sample = len(matches); points = wins * 3 + draws
        return FormWindow(window=size, sample_size=sample, wins=wins, draws=draws, losses=losses, goals_for=gf, goals_against=ga, average_goals_for=round(gf / sample, 3) if sample else 0, average_goals_against=round(ga / sample, 3) if sample else 0, points=points, possible_points=sample * 3, points_percentage=round(points / (sample * 3), 4) if sample else 0, matches=matches)

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
        return MatchSummary(id=f"af-{fixture_id}", competition=str(league.get("name") or "Fútbol"), country=str(league.get("country") or ""), home_team=home_name, away_team=away_name, starts_at=datetime.fromisoformat(starts_at.replace("Z", "+00:00")), status=status, score=score, source="api-football", home_team_id=home.get("id") if isinstance(home.get("id"), int) else None, away_team_id=away.get("id") if isinstance(away.get("id"), int) else None, home_logo=home.get("logo") if isinstance(home.get("logo"), str) else None, away_logo=away.get("logo") if isinstance(away.get("logo"), str) else None, season=league.get("season") if isinstance(league.get("season"), int) else None, round=league.get("round") if isinstance(league.get("round"), str) else None, competition_id=league.get("id") if isinstance(league.get("id"), int) else None, competition_logo=league.get("logo") if isinstance(league.get("logo"), str) else None)
