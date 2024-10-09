"""serial num cols

Revision ID: 27c277f30927
Revises: 88fe4a21a344
Create Date: 2024-10-06 15:53:11.007731

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '27c277f30927'
down_revision: Union[str, None] = '88fe4a21a344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposalcharge', sa.Column('pchg_sr_no', sa.Integer(), nullable=True))
    op.add_column('proposalmotorcert', sa.Column('prai_risk_sr_no', sa.Integer(), nullable=True))
    op.add_column('proposalrisk', sa.Column('prai_risk_sr_no', sa.Integer(), nullable=True))
    op.add_column('proposalsection', sa.Column('psec_srno', sa.Integer(), nullable=True))
    op.add_column('proposalsmi', sa.Column('prs_sr_no', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposalsmi', 'prs_sr_no')
    op.drop_column('proposalsection', 'psec_srno')
    op.drop_column('proposalrisk', 'prai_risk_sr_no')
    op.drop_column('proposalmotorcert', 'prai_risk_sr_no')
    op.drop_column('proposalcharge', 'pchg_sr_no')
    # ### end Alembic commands ###