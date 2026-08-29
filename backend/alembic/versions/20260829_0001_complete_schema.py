"""complete operational and research schema

Revision ID: 20260829_0001
Revises:
Create Date: 2026-08-29
"""
from collections.abc import Sequence

from alembic import op

from app.core.database import Base
from app import models  # noqa: F401

revision: str = "20260829_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    # The initial schema is intentionally sourced from the reviewed metadata so
    # the migration and model registry cannot drift during scaffold development.
    Base.metadata.create_all(bind=op.get_bind(), checkfirst=False)


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind(), checkfirst=True)
