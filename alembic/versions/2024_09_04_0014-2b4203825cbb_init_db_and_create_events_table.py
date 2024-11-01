"""Init db and create events table

Revision ID: 2b4203825cbb
Revises: 
Create Date: 2024-09-04 00:14:08.553858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b4203825cbb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('source', sa.String(length=100), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('splits', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=False),
    sa.Column('courses', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
