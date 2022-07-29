"""Add content column to post table

Revision ID: 547981b4dddc
Revises: b1e56649a05d
Create Date: 2022-07-28 11:52:26.161213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "547981b4dddc"
down_revision = "b1e56649a05d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
