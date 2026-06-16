"""final migration

Revision ID: 4b29bc555ca0
Revises: db9f561232f9
Create Date: 2026-06-16 07:31:23.360627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b29bc555ca0'
down_revision: Union[str, Sequence[str], None] = 'db9f561232f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
