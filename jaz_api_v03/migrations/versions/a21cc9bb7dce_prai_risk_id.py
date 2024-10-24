"""prai_risk_id

Revision ID: a21cc9bb7dce
Revises: 7391d76bd7d6
Create Date: 2024-10-22 13:25:12.932808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a21cc9bb7dce'
down_revision: Union[str, None] = '7391d76bd7d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('proposalcharge', 'chg_sr_no',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('proposalmotorcert', 'prai_risk_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('proposalrisk', 'risk_sr_no',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('proposalrisk', 'prai_risk_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('proposalsmi', 'smi_sr_no',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('proposalsmi', 'smi_sr_no',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('proposalrisk', 'prai_risk_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('proposalrisk', 'risk_sr_no',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('proposalmotorcert', 'prai_risk_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('proposalcharge', 'chg_sr_no',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###