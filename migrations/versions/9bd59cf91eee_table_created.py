"""table created

Revision ID: 9bd59cf91eee
Revises: 2ea7b0a2dbe5
Create Date: 2023-06-28 16:45:53.136821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9bd59cf91eee"
down_revision = "2ea7b0a2dbe5"
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "username", sa.VARCHAR(length=80), autoincrement=False, nullable=False
        ),
        sa.Column("email", sa.VARCHAR(length=120), autoincrement=False, nullable=False),
        sa.Column("add", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("email", name="user_email_key"),
        sa.UniqueConstraint("username", name="user_username_key"),
    )
    op.drop_table("book")
    # ### end Alembic commands ###