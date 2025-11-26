"""Refresh token id removed. JTI primary key now

Revision ID: 243f429ccd35
Revises: 7c8e6277eaee
Create Date: 2025-11-25 22:42:51.968463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '243f429ccd35'
down_revision: Union[str, Sequence[str], None] = '7c8e6277eaee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('refresh_tokens', 'id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('refresh_tokens', sa.Column('id', sa.UUID(), autoincrement=False, nullable=False))
