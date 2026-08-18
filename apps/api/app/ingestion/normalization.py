from datetime import datetime

from app.providers.contracts import ProviderMatch


def normalize_match(
    record: ProviderMatch, competition_id, home_team_id, away_team_id
) -> dict[str, object]:
    """Map a provider match to persistence-ready values while retaining event/available times."""
    return {
        "provider": record.ref.provider,
        "external_id": record.ref.external_id,
        "competition_id": competition_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "starts_at": record.starts_at,
        "status": record.status,
        "source": record.ref.provider,
        "available_at": record.available_at,
        "event_time": record.event_time or record.starts_at,
        "normalized_at": datetime.utcnow(),
    }
