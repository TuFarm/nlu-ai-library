from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import configure_mappers

from app.core.database import Base
from app import models  # noqa: F401


def test_metadata_and_mappers_load():
    configure_mappers()
    assert len(Base.metadata.tables) >= 50
    for table in Base.metadata.sorted_tables:
        str(CreateTable(table).compile(dialect=postgresql.dialect()))


def test_critical_tables_and_relationships():
    required = {"users", "user_sessions", "interaction_events", "books", "book_copies", "search_queries", "ai_requests", "rag_requests", "recommendation_items", "borrowing_records", "audit_logs"}
    assert required <= set(Base.metadata.tables)
    assert Base.metadata.tables["interaction_events"].c.session_id.foreign_keys
    assert Base.metadata.tables["borrowing_records"].c.book_copy_id.foreign_keys


def test_database_constraints_are_declared():
    for name in ("borrowing_records", "ai_requests", "authentication_events", "game_sessions"):
        assert any(isinstance(c, CheckConstraint) for c in Base.metadata.tables[name].constraints)
    for name in ("book_authors", "book_genres"):
        assert len(Base.metadata.tables[name].primary_key.columns) == 2
    assert any(isinstance(c, UniqueConstraint) for c in Base.metadata.tables["search_results"].constraints)


def test_append_only_history_is_not_soft_deletable():
    for name in ("interaction_events", "audit_logs", "system_performance_logs"):
        assert "deleted_at" not in Base.metadata.tables[name].c


def test_destructive_cascades_do_not_target_history():
    for name in ("interaction_events", "audit_logs", "authentication_events", "borrowing_records"):
        for fk in Base.metadata.tables[name].foreign_keys:
            assert fk.ondelete != "CASCADE"


def test_analytics_extension_is_registered_and_additive():
    analytics = {
        "dim_date", "dim_time", "ai_models", "prompt_templates", "staff", "staff_activities",
        "fact_daily_library_usage", "fact_borrowing", "fact_search", "fact_recommendation",
        "fact_ai_usage", "fact_game", "fact_authentication", "fact_survey",
        "dashboard_metrics", "alert_rules", "dashboards", "ml_datasets", "training_runs",
    }
    assert analytics <= set(Base.metadata.tables)
    assert len(Base.metadata.tables) == 92
    assert Base.metadata.tables["ai_requests"].c.ai_model_id.foreign_keys
    assert Base.metadata.tables["ai_requests"].c.prompt_template_id.foreign_keys


def test_fact_grains_and_dashboard_indexes():
    for name in ("fact_borrowing", "fact_search", "fact_recommendation", "fact_ai_usage"):
        assert any(isinstance(c, UniqueConstraint) for c in Base.metadata.tables[name].constraints)
    popularity_indexes = {index.name for index in Base.metadata.tables["book_popularity_snapshots"].indexes}
    assert "ix_book_popularity_date_score" in popularity_indexes
