"""Adding topscorer and winner to tournament model

Revision ID: 68835c25e25b
Revises: 7851c2230093
Create Date: 2026-06-12 00:23:10.326550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68835c25e25b'
down_revision: Union[str, Sequence[str], None] = '7851c2230093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tournaments', sa.Column('winner', sa.String(length=50), nullable=True))
    op.add_column('tournaments', sa.Column('top_scorer', sa.String(length=50), nullable=True))

def downgrade() -> None:
    op.drop_column('tournaments', 'top_scorer')
    op.drop_column('tournaments', 'winner')