"""Created_at add to users

Revision ID: a26f2a3a44b7
Revises: ba0b0d1d6d26
Create Date: 2025-10-02 01:30:17.356141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a26f2a3a44b7'
down_revision: Union[str, Sequence[str], None] = 'ba0b0d1d6d26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'created_at')

