"""initial normalized sports domain

Revision ID: 20260818_0001
Revises:
Create Date: 2026-08-18
"""

import sqlalchemy as sa

from alembic import op

revision = "20260818_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sports",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(80), nullable=False, unique=True),
    )
    op.create_table(
        "data_providers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("is_mock", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        "countries",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("code", sa.String(3), nullable=False, unique=True),
    )
    op.create_table(
        "competitions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("sport_id", sa.Uuid(), sa.ForeignKey("sports.id"), nullable=False),
        sa.Column("country_id", sa.Uuid(), sa.ForeignKey("countries.id")),
        sa.Column("name", sa.String(160), nullable=False),
    )
    op.create_table(
        "seasons",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("competition_id", sa.Uuid(), sa.ForeignKey("competitions.id"), nullable=False),
        sa.Column("name", sa.String(40), nullable=False),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("sport_id", sa.Uuid(), sa.ForeignKey("sports.id"), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("country_id", sa.Uuid(), sa.ForeignKey("countries.id")),
    )
    op.create_table(
        "venues",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("city", sa.String(120)),
        sa.Column("capacity", sa.Integer()),
    )
    op.create_table(
        "players",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("team_id", sa.Uuid(), sa.ForeignKey("teams.id")),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("position", sa.String(40)),
    )
    op.create_table(
        "matches",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("competition_id", sa.Uuid(), sa.ForeignKey("competitions.id"), nullable=False),
        sa.Column("season_id", sa.Uuid(), sa.ForeignKey("seasons.id")),
        sa.Column("venue_id", sa.Uuid(), sa.ForeignKey("venues.id")),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(40), nullable=False),
    )
    op.create_table(
        "match_teams",
        sa.Column("match_id", sa.Uuid(), sa.ForeignKey("matches.id"), primary_key=True),
        sa.Column("team_id", sa.Uuid(), sa.ForeignKey("teams.id"), primary_key=True),
        sa.Column("side", sa.String(8), nullable=False),
        sa.Column("score", sa.Integer()),
    )
    op.create_table(
        "match_statistics",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("match_id", sa.Uuid(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("team_id", sa.Uuid(), sa.ForeignKey("teams.id")),
        sa.Column("metric", sa.String(80), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True)),
        sa.Column("available_at", sa.DateTime(timezone=True)),
        sa.Column("source", sa.String(40), nullable=False),
    )
    op.create_table(
        "player_statistics",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("match_id", sa.Uuid(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("player_id", sa.Uuid(), sa.ForeignKey("players.id"), nullable=False),
        sa.Column("metric", sa.String(80), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
    )
    op.create_table(
        "bookmakers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
    )
    op.create_table(
        "markets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("sport_id", sa.Uuid(), sa.ForeignKey("sports.id"), nullable=False),
        sa.Column("key", sa.String(100), nullable=False, unique=True),
        sa.Column("name", sa.String(160), nullable=False),
    )
    op.create_table(
        "market_selections",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("market_id", sa.Uuid(), sa.ForeignKey("markets.id"), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("line", sa.Float()),
    )
    op.create_table(
        "odds_snapshots",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("match_id", sa.Uuid(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("selection_id", sa.Uuid(), sa.ForeignKey("market_selections.id"), nullable=False),
        sa.Column("bookmaker_id", sa.Uuid(), sa.ForeignKey("bookmakers.id"), nullable=False),
        sa.Column("decimal_odds", sa.Float(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(40), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_table("odds_snapshots")
    op.drop_table("market_selections")
    op.drop_table("markets")
    op.drop_table("bookmakers")
    op.drop_table("player_statistics")
    op.drop_table("match_statistics")
    op.drop_table("match_teams")
    op.drop_table("matches")
    op.drop_table("players")
    op.drop_table("venues")
    op.drop_table("teams")
    op.drop_table("seasons")
    op.drop_table("competitions")
    op.drop_table("countries")
    op.drop_table("data_providers")
    op.drop_table("sports")
