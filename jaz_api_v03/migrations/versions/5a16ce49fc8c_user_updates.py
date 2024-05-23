"""user updates

Revision ID: 5a16ce49fc8c
Revises: 704a10191acd
Create Date: 2024-05-23 15:45:39.126150

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5a16ce49fc8c"
down_revision: Union[str, None] = "704a10191acd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("nic", sa.String(), nullable=True))
    op.add_column("user", sa.Column("pin", sa.String(), nullable=True))
    op.alter_column("user", "password", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("user", "phone", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("user", "client_code")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "client_code", sa.VARCHAR(length=10), autoincrement=False, nullable=True
        ),
    )  # noqa: E501
    op.alter_column("user", "phone", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("user", "password", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column("user", "pin")
    op.drop_column("user", "nic")
    # ### end Alembic commands ###
