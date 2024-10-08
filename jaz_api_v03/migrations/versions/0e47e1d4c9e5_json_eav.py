"""JSON EAV

Revision ID: 0e47e1d4c9e5
Revises: 064972b3741a
Create Date: 2024-09-12 16:03:24.239103

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0e47e1d4c9e5'
down_revision: Union[str, None] = '064972b3741a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jsonattribute',
    sa.Column('json_attr_sys_id', sa.Integer(), nullable=False),
    sa.Column('entity_type', sa.String(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('attr_sys_id', sa.Integer(), nullable=False),
    sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('value_code', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attr_sys_id'], ['attributedefinition.attr_sys_id'], ),
    sa.PrimaryKeyConstraint('json_attr_sys_id'),
    sa.UniqueConstraint('entity_type', 'entity_id', 'attr_sys_id')
    )
    op.create_index(op.f('ix_jsonattribute_json_attr_sys_id'), 'jsonattribute', ['json_attr_sys_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jsonattribute_json_attr_sys_id'), table_name='jsonattribute')
    op.drop_table('jsonattribute')
    # ### end Alembic commands ###
