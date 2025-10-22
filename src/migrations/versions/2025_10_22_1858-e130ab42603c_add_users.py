"""add users

Revision ID: e130ab42603c
Revises: 3db03b13991d
Create Date: 2025-10-22 18:58:54.861042

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e130ab42603c"
down_revision: Union[str, Sequence[str], None] = "3db03b13991d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
