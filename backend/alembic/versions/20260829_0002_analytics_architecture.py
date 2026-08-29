"""add analytics, BI, dashboard, staff and ML architecture

Revision ID: 20260829_0002
Revises: 20260829_0001
Create Date: 2026-08-29
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.core.database import Base
from app import models  # noqa: F401

revision: str = "20260829_0002"
down_revision: str | None = "20260829_0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

NEW_TABLES = {
    "dim_date", "dim_time", "ai_models", "prompt_templates", "departments", "roles", "permissions",
    "role_permissions", "staff", "staff_roles", "staff_activities", "faculties", "majors", "courses",
    "student_academic_profiles", "course_enrollments", "reading_rooms", "location_traffic_snapshots",
    "fact_daily_library_usage", "fact_borrowing", "fact_search", "fact_recommendation", "fact_ai_usage",
    "fact_game", "fact_authentication", "fact_survey", "book_popularity_snapshots", "dashboard_metrics",
    "alert_rules", "alert_history", "dashboards", "dashboard_widgets", "widget_layouts", "widget_filters",
    "saved_filters", "user_dashboard_preferences", "ml_datasets", "dataset_versions", "ml_experiments",
    "feature_sets", "training_runs", "evaluation_metrics",
}


def upgrade() -> None:
    bind = op.get_bind()
    # Revision 0001 predates a frozen explicit operation list and imports live
    # metadata. Consequently a brand-new installation already receives these
    # tables from 0001. Existing installations do not. Inspecting makes this
    # revision safe in both cases; offline SQL is fully emitted by 0001.
    if op.get_context().as_sql:
        return
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())
    for table in Base.metadata.sorted_tables:
        if table.name in NEW_TABLES and table.name not in existing_tables:
            table.create(bind=bind, checkfirst=False)
    ai_columns = {column["name"] for column in inspector.get_columns("ai_requests")}
    if "ai_model_id" not in ai_columns:
        op.add_column("ai_requests", sa.Column("ai_model_id", postgresql.UUID(as_uuid=True), nullable=True))
        op.create_foreign_key("fk_ai_requests_ai_model", "ai_requests", "ai_models", ["ai_model_id"], ["id"], ondelete="RESTRICT")
        op.create_index("ix_ai_requests_ai_model_id", "ai_requests", ["ai_model_id"])
    if "prompt_template_id" not in ai_columns:
        op.add_column("ai_requests", sa.Column("prompt_template_id", postgresql.UUID(as_uuid=True), nullable=True))
        op.create_foreign_key("fk_ai_requests_prompt_template", "ai_requests", "prompt_templates", ["prompt_template_id"], ["id"], ondelete="RESTRICT")
        op.create_index("ix_ai_requests_prompt_template_id", "ai_requests", ["prompt_template_id"])


def downgrade() -> None:
    bind = op.get_bind()
    if not op.get_context().as_sql:
        inspector = sa.inspect(bind)
        ai_columns = {column["name"] for column in inspector.get_columns("ai_requests")}
        foreign_keys = {tuple(fk["constrained_columns"]): fk["name"] for fk in inspector.get_foreign_keys("ai_requests")}
        if "prompt_template_id" in ai_columns:
            op.drop_index("ix_ai_requests_prompt_template_id", table_name="ai_requests")
            op.drop_constraint(foreign_keys[("prompt_template_id",)], "ai_requests", type_="foreignkey")
            op.drop_column("ai_requests", "prompt_template_id")
        if "ai_model_id" in ai_columns:
            op.drop_index("ix_ai_requests_ai_model_id", table_name="ai_requests")
            op.drop_constraint(foreign_keys[("ai_model_id",)], "ai_requests", type_="foreignkey")
            op.drop_column("ai_requests", "ai_model_id")
    for table in reversed(Base.metadata.sorted_tables):
        if table.name in NEW_TABLES and (op.get_context().as_sql or sa.inspect(bind).has_table(table.name)):
            table.drop(bind=bind, checkfirst=not op.get_context().as_sql)
