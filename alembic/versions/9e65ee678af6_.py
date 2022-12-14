"""empty message

Revision ID: 9e65ee678af6
Revises: 
Create Date: 2022-10-17 17:49:15.303217

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "9e65ee678af6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "competition",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("title", sa.VARCHAR(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "race",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("race_nr", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "competitor",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=128), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=256), nullable=False),
        sa.Column(
            "country",
            sa.Enum("GER", "GRE", "ITA", "NL", name="country"),
            nullable=False,
        ),
        sa.Column("sail_nr", sa.BigInteger(), nullable=False),
        sa.Column("total_points", sa.BigInteger(), nullable=False),
        sa.Column("net_points", sa.BigInteger(), nullable=False),
        sa.Column(
            "club", sa.Enum("NOC", "ANOG", "SEANATK", name="club"), nullable=False
        ),
        sa.Column("competition_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["competition_id"],
            ["competition.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "position",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("points", sa.BigInteger(), nullable=False),
        sa.Column("race_id", postgresql.UUID(), nullable=True),
        sa.Column("competitor_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["competitor_id"],
            ["competitor.id"],
        ),
        sa.ForeignKeyConstraint(
            ["race_id"],
            ["race.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("position")
    op.drop_table("competitor")
    op.drop_table("race")
    op.drop_table("competition")
    # ### end Alembic commands ###
