"""ERROR LOG

Revision ID: 57885dbff9f9
Revises: 0e47e1d4c9e5
Create Date: 2024-09-15 11:34:13.024250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57885dbff9f9'
down_revision: Union[str, None] = '0e47e1d4c9e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('errorlog',
    sa.Column('error_log_sys_id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('error_log', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('error_log_sys_id')
    )
    op.create_index(op.f('ix_errorlog_error_log_sys_id'), 'errorlog', ['error_log_sys_id'], unique=False)
    op.create_unique_constraint(None, 'jsonattribute', ['entity_type', 'entity_id', 'attr_sys_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'jsonattribute', type_='unique')
    op.drop_index(op.f('ix_errorlog_error_log_sys_id'), table_name='errorlog')
    op.drop_table('errorlog')
    # ### end Alembic commands ###
