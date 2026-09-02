"""initial optimized AI kiosk assistant schema

Revision ID: 20260902_0001
Revises:
Create Date: 2026-09-02
"""
from collections.abc import Sequence

from alembic import op

from app import models  # noqa: F401
from app.core.database import Base

revision: str = "20260902_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


EXPECTED_TABLES = {
    "users",
    "user_preferences",
    "face_profiles",
    "face_authentication_logs",
    "devices",
    "user_sessions",
    "interaction_events",
    "knowledge_sources",
    "knowledge_documents",
    "knowledge_chunks",
    "conversations",
    "conversation_messages",
    "ai_requests",
    "ai_responses",
    "ai_feedback",
    "prompt_versions",
    "book_categories",
    "suggested_books",
    "book_suggestion_logs",
    "surveys",
    "survey_questions",
    "survey_responses",
    "survey_answers",
    "daily_report_metrics",
}


def _validated_tables():
    actual = set(Base.metadata.tables)
    if actual != EXPECTED_TABLES:
        raise RuntimeError(
            f"Migration expects exactly 24 AI kiosk tables; missing={EXPECTED_TABLES-actual}, "
            f"unexpected={actual-EXPECTED_TABLES}"
        )
    return Base.metadata.sorted_tables


def upgrade() -> None:
    bind = op.get_bind()
    for table in _validated_tables():
        table.create(bind=bind, checkfirst=False)


def downgrade() -> None:
    bind = op.get_bind()
    for table in reversed(_validated_tables()):
        table.drop(bind=bind, checkfirst=False)
