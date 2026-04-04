"""create room table and seed rooms

Revision ID: 20260404140000
Revises: 20260404130000
Create Date: 2026-04-04

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table

revision: str = "20260404140000"
down_revision: Union[str, None] = "20260404130000"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Stable IDs for seed rows (referenced by tests / predictable data)
ROOM_TRAVEL_ID = "11111111-1111-4111-8111-111111111111"
ROOM_DATING_ID = "22222222-2222-4222-8222-222222222222"
ROOM_BUSINESS_ID = "33333333-3333-4333-8333-333333333333"


def upgrade() -> None:
    op.create_table(
        "room",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("invite_link", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    room = table(
        "room",
        column("id", postgresql.UUID(as_uuid=True)),
        column("name", sa.String()),
        column("topic", sa.String()),
        column("invite_link", sa.String()),
    )
    op.bulk_insert(
        room,
        [
            {
                "id": ROOM_TRAVEL_ID,
                "name": "Travel",
                "topic": "Travel and culture",
                "invite_link": "https://t.me/+placeholderTravelRoom",
            },
            {
                "id": ROOM_DATING_ID,
                "name": "Dating",
                "topic": "Dating and social life",
                "invite_link": "https://t.me/+placeholderDatingRoom",
            },
            {
                "id": ROOM_BUSINESS_ID,
                "name": "Business",
                "topic": "Work and business English",
                "invite_link": "https://t.me/+placeholderBusinessRoom",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("room")
