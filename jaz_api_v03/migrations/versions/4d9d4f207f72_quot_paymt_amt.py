"""quot_paymt_amt

Revision ID: 4d9d4f207f72
Revises: 27c277f30927
Create Date: 2024-10-15 13:39:50.913183

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4d9d4f207f72'
down_revision: Union[str, None] = '27c277f30927'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposal', sa.Column('prop_paymt_amt', sa.Float(), nullable=True))
    # op.alter_column('proposalcharge', 'pchg_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('proposalcover', 'prc_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('proposalmotorcert', 'prai_risk_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('proposalrisk', 'prai_risk_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('proposalsection', 'psec_srno',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('proposalsmi', 'prs_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    op.add_column('quote', sa.Column('quot_paymt_amt', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quote', 'quot_paymt_amt')
    # op.alter_column('proposalsmi', 'prs_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('proposalsection', 'psec_srno',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('proposalrisk', 'prai_risk_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('proposalmotorcert', 'prai_risk_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('proposalcover', 'prc_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('proposalcharge', 'pchg_sr_no',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    op.drop_column('proposal', 'prop_paymt_amt')
    # ### end Alembic commands ###
