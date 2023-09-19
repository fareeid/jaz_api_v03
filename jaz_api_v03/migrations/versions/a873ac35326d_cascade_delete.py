"""Cascade delete

Revision ID: a873ac35326d
Revises: af2a140d5262
Create Date: 2023-09-19 12:54:27.578178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a873ac35326d"
down_revision: Union[str, None] = "af2a140d5262"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("item_owner_id_fkey", "item", type_="foreignkey")
    op.create_foreign_key(
        None,
        "item",
        "person",
        ["owner_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "item", type_="foreignkey")
    op.create_foreign_key("item_owner_id_fkey", "item", "person", ["owner_id"], ["id"])
    # ### end Alembic commands ###
