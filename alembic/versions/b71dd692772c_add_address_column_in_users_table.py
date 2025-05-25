"""Add address column in Users table

Revision ID: b71dd692772c
Revises: 63703464b242
Create Date: 2025-05-19 16:06:28.426235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b71dd692772c'
down_revision: Union[str, None] = '63703464b242'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('address',sa.String(255),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','address')
