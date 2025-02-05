"""Quote Gender and DOB

Revision ID: 128ad688aae5
Revises: 57885dbff9f9
Create Date: 2024-09-22 01:47:06.191411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '128ad688aae5'
down_revision: Union[str, None] = '57885dbff9f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote', sa.Column('quot_assr_gender', sa.String(), nullable=True))
    op.add_column('quote', sa.Column('quot_assr_dob', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quote', 'quot_assr_dob')
    op.drop_column('quote', 'quot_assr_gender')
    # ### end Alembic commands ###
