"""rename field for rooms_facilities

Revision ID: b2b30c2554a4
Revises: 8229efabb967
Create Date: 2025-11-29 22:18:56.733612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2b30c2554a4"
down_revision: Union[str, Sequence[str], None] = "8229efabb967"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "room_facilities", sa.Column("facility_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        op.f("room_facilities_facilities_id_fkey"),
        "room_facilities",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "room_facilities", "facilities", ["facility_id"], ["id"]
    )
    op.drop_column("room_facilities", "facilities_id")


def downgrade() -> None:
    op.add_column(
        "room_facilities",
        sa.Column("facilities_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "room_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("room_facilities_facilities_id_fkey"),
        "room_facilities",
        "facilities",
        ["facilities_id"],
        ["id"],
    )
    op.drop_column("room_facilities", "facility_id")
