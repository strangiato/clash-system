"""adding player

Revision ID: 394e5a8ba217
Revises: 65ce9f90cb12
Create Date: 2020-09-07 21:11:46.720359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "394e5a8ba217"
down_revision = "65ce9f90cb12"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "player",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("tag", sa.String(length=80), nullable=False),
        sa.Column("trophies", sa.Integer(), nullable=True),
        sa.Column("best_trophies", sa.Integer(), nullable=True),
        sa.Column("donations", sa.Integer(), nullable=False),
        sa.Column("donations_received", sa.Integer(), nullable=False),
        sa.Column("battle_count", sa.Integer(), nullable=True),
        sa.Column("three_crown_wins", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tag"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("player")
    # ### end Alembic commands ###