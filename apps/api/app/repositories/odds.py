"""Persistence boundary for append-only odds snapshots.

Provider adapters call `append`, never an update method, to preserve price history.
"""

from app.infrastructure.models import OddsSnapshot


class OddsSnapshotRepository:
    def __init__(self, session) -> None:  # SQLAlchemy Session kept untyped at infrastructure seam
        self.session = session

    def append(self, snapshot: OddsSnapshot) -> OddsSnapshot:
        self.session.add(snapshot)
        self.session.flush()
        return snapshot
