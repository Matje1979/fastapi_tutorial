"""add foreign-key to posts table

Revision ID: 10d4d4db51f3
Revises: 7b918d54afb2
Create Date: 2022-07-28 13:19:40.371747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10d4d4db51f3"
down_revision = "7b918d54afb2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
