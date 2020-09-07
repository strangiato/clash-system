"""empty message

Revision ID: 65ce9f90cb12
Revises: 3c403aee5d08
Create Date: 2020-09-07 20:46:30.524254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "65ce9f90cb12"
down_revision = "3c403aee5d08"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("clanname", sa.String(length=80), nullable=False),
        sa.Column("tag", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("required_trophies", sa.Integer(), nullable=False),
        sa.Column("clan_score", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tag"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("clan")
    # ### end Alembic commands ###