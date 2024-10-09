"""Transaction defaults

Revision ID: baa0ba22de81
Revises: 128ad688aae5
Create Date: 2024-09-24 19:41:10.639925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'baa0ba22de81'
down_revision: Union[str, None] = '128ad688aae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('pol_trans_dflt', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('productchargeassociation', sa.Column('chg_trans_dflt', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('productsectionassociation', sa.Column('sec_trans_dflt', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('sectioncoverassociation', sa.Column('cvr_trans_dflt', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sectioncoverassociation', 'cvr_trans_dflt')
    op.drop_column('productsectionassociation', 'sec_trans_dflt')
    op.drop_column('productchargeassociation', 'chg_trans_dflt')
    op.drop_column('product', 'pol_trans_dflt')
    # ### end Alembic commands ###