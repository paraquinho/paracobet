from collections.abc import Iterable
from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class IngestionReport:
    entity: str
    fetched: int
    validated: int
    persisted: int
    skipped: int


def validate_records(records: Iterable[BaseModel]) -> list[BaseModel]:
    """Provider Pydantic models validate at construction; this stage enforces a list boundary."""
    return list(records)


def normalize_records(records: Iterable[BaseModel]) -> list[dict[str, object]]:
    return [record.model_dump(mode="json") for record in records]


def ingest(entity: str, fetch: callable, persist: callable) -> IngestionReport:
    """Run stages; idempotent behavior is delegated to the persistence callback."""
    fetched_records = list(fetch())
    validated = validate_records(fetched_records)
    normalized = normalize_records(validated)
    persisted, skipped = persist(normalized)
    return IngestionReport(entity, len(fetched_records), len(validated), persisted, skipped)
