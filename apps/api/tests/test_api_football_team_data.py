from app.providers.api_football import ApiFootballProvider


def fixture(fixture_id: int, league_id: int = 39, season: int = 2025, home_id: int = 10, away_id: int = 20) -> dict:
    return {
        "fixture": {"id": fixture_id, "date": "2025-08-10T15:00:00+00:00"},
        "league": {"id": league_id, "name": "Premier League", "season": season},
        "teams": {"home": {"id": home_id, "name": "Alpha FC"}, "away": {"id": away_id, "name": "Beta FC"}},
        "goals": {"home": 2, "away": 1},
    }


def test_form_normalizes_context_and_home_away() -> None:
    result = ApiFootballProvider._normalize_form(fixture(1), 10, 39, 2025)
    assert result is not None
    assert result.competition_id == 39
    assert result.is_home is True
    assert result.result == "W"
    assert result.goals_for == 2
    assert result.goals_against == 1


def test_form_discards_wrong_competition_and_season() -> None:
    provider = ApiFootballProvider()
    assert provider._normalize_form(fixture(2, league_id=140), 10, 39, 2025) is None
    assert provider._normalize_form(fixture(3, season=2024), 10, 39, 2025) is None
    assert provider._normalize_form({**fixture(4), "fixture": {"date": "2025-08-10T15:00:00+00:00"}}, 10, 39, 2025) is None


def test_form_windows_and_real_team_name(monkeypatch) -> None:
    provider = ApiFootballProvider()
    payload = {"response": [fixture(i) for i in range(1, 21)]}
    monkeypatch.setattr(provider, "_request", lambda resource, params: payload)
    result = provider.get_team_form(10, 39, 2025)
    assert result.team_name == "Alpha FC"
    assert [result.windows[f"L{size}"].sample_size for size in (5, 10, 15, 20)] == [5, 10, 15, 20]


def test_statistics_preserves_provider_team_name(monkeypatch) -> None:
    provider = ApiFootballProvider()
    monkeypatch.setattr(provider, "_request", lambda resource, params: {"response": {"team": {"id": 10, "name": "Alpha FC", "logo": None}, "fixtures": {}, "goals": {}}})
    result = provider.get_team_statistics(10, 39, 2025)
    assert result.team_name == "Alpha FC"
