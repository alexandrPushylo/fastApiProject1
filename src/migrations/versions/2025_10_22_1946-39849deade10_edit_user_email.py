"""edit user.email

Revision ID: 39849deade10
Revises: e130ab42603c
Create Date: 2025-10-22 19:46:23.796064

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39849deade10"
down_revision: Union[str, Sequence[str], None] = "e130ab42603c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('users_email_key', "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('users_email_key', "users", type_="unique")
