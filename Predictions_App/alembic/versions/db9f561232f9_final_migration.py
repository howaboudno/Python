"""final migration

Revision ID: db9f561232f9
Revises: 68835c25e25b
Create Date: 2026-06-16 07:19:35.199054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db9f561232f9'
down_revision: Union[str, Sequence[str], None] = '68835c25e25b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
