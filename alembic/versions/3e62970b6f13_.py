"""empty message

Revision ID: 3e62970b6f13
Revises: b9a6ee6eba04
Create Date: 2022-10-18 08:51:55.483640

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3e62970b6f13"
down_revision = "b9a6ee6eba04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "competitor",
        "total_points",
        existing_type=sa.BIGINT(),
        server_default="0",
        existing_nullable=False,
    )
    op.alter_column(
        "competitor",
        "net_points",
        existing_type=sa.BIGINT(),
        server_default="0",
        existing_nullable=False,
    )
    op.create_index(op.f("ix_competitor_club"), "competitor", ["club"], unique=False)
    op.create_index(
        op.f("ix_competitor_sail_nr"), "competitor", ["sail_nr"], unique=False
    )
    op.create_index(op.f("ix_race_race_nr"), "race", ["race_nr"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_race_race_nr"), table_name="race")
    op.drop_index(op.f("ix_competitor_sail_nr"), table_name="competitor")
    op.drop_index(op.f("ix_competitor_club"), table_name="competitor")
    op.alter_column(
        "competitor",
        "net_points",
        existing_type=sa.BIGINT(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "competitor",
        "total_points",
        existing_type=sa.BIGINT(),
        server_default=None,
        existing_nullable=False,
    )
    # ### end Alembic commands ###
