"""initial migration with users table phone_num column

Revision ID: 63703464b242
Revises: 
Create Date: 2025-05-19 15:43:11.475520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63703464b242'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.add_column('users', sa.Column('Phone_number',sa.String(10),nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
