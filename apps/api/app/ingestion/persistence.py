from collections.abc import Iterable

from sqlalchemy import select

from app.infrastructure.models import Match


def persist_matches(session, records: Iterable[dict[str, object]]) -> tuple[int, int]:
    """Persist normalized matches idempotently using `(provider, external_id)`."""
    inserted = skipped = 0
    for record in records:
        ref = record["ref"]
        provider, external_id = ref["provider"], ref["external_id"]
        exists = session.scalar(
            select(Match.id).where(Match.provider == provider, Match.external_id == external_id)
        )
        if exists:
            skipped += 1
            continue
        session.add(
            Match(
                provider=provider,
                external_id=external_id,
                competition_id=record["competition_id"],
                status=record["status"],
                starts_at=record["starts_at"],
                source=provider,
                available_at=record["available_at"],
            )
        )
        inserted += 1
    session.commit()
    return inserted, skipped
