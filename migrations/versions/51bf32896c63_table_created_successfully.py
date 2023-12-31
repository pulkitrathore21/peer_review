"""table created successfully

Revision ID: 51bf32896c63
Revises: 0aa972af06d3
Create Date: 2023-06-28 18:11:29.936075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "51bf32896c63"
down_revision = "0aa972af06d3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("authur_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.TEXT(), nullable=True),
        sa.Column("cover_image", sa.TEXT(), nullable=True),
        sa.Column("pages", sa.Integer(), nullable=True),
        sa.Column("releasedate", sa.TEXT(), nullable=True),
        sa.Column("isbn", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # op.drop_table('practice_pokemon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "practice_pokemon",
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("color", sa.TEXT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("name", name="practice_pokemon_pkey"),
    )
    op.drop_table("book")
    # ### end Alembic commands ###
