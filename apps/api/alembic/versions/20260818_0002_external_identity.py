"""add provider identities and availability timestamps

Revision ID: 20260818_0002
Revises: 20260818_0001
"""

import sqlalchemy as sa

from alembic import op

revision = "20260818_0002"
down_revision = "20260818_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table in ("competitions", "teams", "matches", "bookmakers", "markets", "market_selections"):
        op.add_column(
            table, sa.Column("provider", sa.String(80), nullable=False, server_default="internal")
        )
        op.add_column(table, sa.Column("external_id", sa.String(160)))
    op.add_column("matches", sa.Column("available_at", sa.DateTime(timezone=True)))
    op.create_unique_constraint(
        "uq_competition_provider_external", "competitions", ["provider", "external_id"]
    )
    op.create_unique_constraint("uq_team_provider_external", "teams", ["provider", "external_id"])
    op.create_unique_constraint(
        "uq_match_provider_external", "matches", ["provider", "external_id"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_match_provider_external", "matches", type_="unique")
    op.drop_constraint("uq_team_provider_external", "teams", type_="unique")
    op.drop_constraint("uq_competition_provider_external", "competitions", type_="unique")
    op.drop_column("matches", "available_at")
    for table in ("competitions", "teams", "matches", "bookmakers", "markets", "market_selections"):
        op.drop_column(table, "external_id")
        op.drop_column(table, "provider")
