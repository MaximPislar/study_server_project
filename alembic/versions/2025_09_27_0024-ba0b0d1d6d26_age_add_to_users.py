"""Age add to users

Revision ID: ba0b0d1d6d26
Revises: 768ce1dd967a
Create Date: 2025-09-27 00:24:02.372941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba0b0d1d6d26'
down_revision: Union[str, Sequence[str], None] = '768ce1dd967a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'age')
