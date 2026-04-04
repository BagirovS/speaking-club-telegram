"""add users.level

Revision ID: 20260404130000
Revises: 20260404120000
Create Date: 2026-04-04

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260404130000"
down_revision: Union[str, None] = "20260404120000"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("level", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "level")
