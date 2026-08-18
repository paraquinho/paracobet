"""Read repository for normalized match data persisted in PostgreSQL."""

from sqlalchemy import select

from app.domain.entities import MatchSummary
from app.infrastructure.models import Competition, Country, Match, MatchTeam, Team


class MatchRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def list_summaries(self) -> list[MatchSummary]:
        with self.session_factory() as session:
            rows = session.execute(
                select(Match, Competition, Country, MatchTeam, Team)
                .join(Competition, Competition.id == Match.competition_id)
                .outerjoin(Country, Country.id == Competition.country_id)
                .join(MatchTeam, MatchTeam.match_id == Match.id)
                .join(Team, Team.id == MatchTeam.team_id)
                .order_by(Match.starts_at)
            ).all()
        grouped: dict[str, dict[str, object]] = {}
        for match, competition, country, participant, team in rows:
            public_id = match.external_id or str(match.id)
            item = grouped.setdefault(
                public_id,
                {
                    "id": public_id,
                    "competition": competition.name,
                    "country": country.name if country else "",
                    "starts_at": match.starts_at,
                    "status": match.status,
                    "source": match.source,
                    "home_team": "",
                    "away_team": "",
                    "score": None,
                },
            )
            item[f"{participant.side}_team"] = team.name
        return [MatchSummary.model_validate(item) for item in grouped.values()]
