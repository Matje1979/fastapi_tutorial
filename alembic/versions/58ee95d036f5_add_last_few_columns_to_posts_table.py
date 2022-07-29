"""Add last few columns to posts table

Revision ID: 58ee95d036f5
Revises: 10d4d4db51f3
Create Date: 2022-07-28 13:41:16.977841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "58ee95d036f5"
down_revision = "10d4d4db51f3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="True"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
