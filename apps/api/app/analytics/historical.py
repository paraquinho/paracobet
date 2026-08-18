from collections.abc import Sequence

from app.analytics.statistics import historical_summary

WINDOWS = (5, 10, 15, 20)


def historical_window(
    values: Sequence[float], window: int = 5, venue: str = "all", line: float | None = None
) -> dict[str, float | list[float] | str | int]:
    if window not in WINDOWS:
        raise ValueError(f"window must be one of {WINDOWS}")
    if venue not in {"all", "home", "away"}:
        raise ValueError("venue must be all, home or away")
    selected = list(values)[-window:]
    summary = historical_summary(selected, line)
    return {**summary, "window": window, "venue": venue}
