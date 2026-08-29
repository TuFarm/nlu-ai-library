from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, Float, ForeignKey, Index, Integer, LargeBinary, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, SoftDeleteMixin, TimestampMixin
from app.models.enums import *


def enum_col(cls: type[DBEnum], **kw: Any):
    return mapped_column(Enum(cls, name=cls.__name__.lower(), native_enum=False, length=40), **kw)


class UUIDPK:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class User(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"
    student_code: Mapped[str | None] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    user_type: Mapped[UserType] = enum_col(UserType, default=UserType.STUDENT)
    account_status: Mapped[AccountStatus] = enum_col(AccountStatus, default=AccountStatus.ACTIVE, index=True)
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    preferred_language: Mapped[str] = mapped_column(String(10), default="vi")
    sessions: Mapped[list[UserSession]] = relationship(back_populates="user")
    borrowings: Mapped[list[BorrowingRecord]] = relationship(back_populates="user")


class UserPreference(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="user_preferences"; __table_args__=(UniqueConstraint("user_id"),)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    preferred_input_method: Mapped[InputMethod | None]=enum_col(InputMethod, nullable=True)
    language: Mapped[str | None]=mapped_column(String(10)); reading_preferences: Mapped[dict[str,Any]|None]=mapped_column(JSONB); accessibility_preferences: Mapped[dict[str,Any]|None]=mapped_column(JSONB)


class ResearchParticipantProfile(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="research_participant_profiles"; __table_args__=(UniqueConstraint("user_id"),)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    anonymous_code: Mapped[str]=mapped_column(String(64), unique=True); demographics: Mapped[dict[str,Any]|None]=mapped_column(JSONB)


class ConsentRecord(UUIDPK, TimestampMixin, Base):
    __tablename__="consent_records"; __table_args__=(Index("ix_consent_user_time","user_id","granted_at"),)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    consent_type: Mapped[str]=mapped_column(String(80)); consent_version: Mapped[str]=mapped_column(String(30)); granted: Mapped[bool]=mapped_column(Boolean)
    granted_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); revoked_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); privacy_policy_version: Mapped[str]=mapped_column(String(30))
    research_use_allowed: Mapped[bool]=mapped_column(Boolean, default=False); biometric_use_allowed: Mapped[bool]=mapped_column(Boolean, default=False); analytics_use_allowed: Mapped[bool]=mapped_column(Boolean, default=False)
    retention_until: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); supersedes_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("consent_records.id"))


class DataSubjectRequest(UUIDPK, TimestampMixin, Base):
    __tablename__="data_subject_requests"
    user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); request_type: Mapped[str]=mapped_column(String(40)); status: Mapped[str]=mapped_column(String(40), index=True); requested_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); anonymized_participant_code: Mapped[str|None]=mapped_column(String(64))


class FaceProfile(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="face_profiles"; __table_args__=(CheckConstraint("quality_score IS NULL OR (quality_score >= 0 AND quality_score <= 1)"),)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True); encrypted_embedding: Mapped[bytes|None]=mapped_column(LargeBinary); secure_reference: Mapped[str|None]=mapped_column(String(500)); model_name: Mapped[str]=mapped_column(String(100)); model_version: Mapped[str]=mapped_column(String(50)); embedding_version: Mapped[str]=mapped_column(String(50)); quality_score: Mapped[float|None]=mapped_column(Float); enrolled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); last_updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); active: Mapped[bool]=mapped_column(Boolean, default=True); revoked_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); retention_until: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))


class LibraryLocation(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="library_locations"
    name: Mapped[str]=mapped_column(String(150)); code: Mapped[str]=mapped_column(String(50), unique=True); address: Mapped[str|None]=mapped_column(String(500)); floor: Mapped[str|None]=mapped_column(String(30)); zone: Mapped[str|None]=mapped_column(String(80))


class Device(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="devices"
    code: Mapped[str]=mapped_column(String(80), unique=True); name: Mapped[str]=mapped_column(String(150)); device_type: Mapped[DeviceType]=enum_col(DeviceType, index=True); location_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("library_locations.id", ondelete="SET NULL")); hardware_version: Mapped[str|None]=mapped_column(String(80)); software_version: Mapped[str|None]=mapped_column(String(80)); status: Mapped[DeviceStatus]=enum_col(DeviceStatus, default=DeviceStatus.OFFLINE); last_seen_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); floor: Mapped[str|None]=mapped_column(String(30)); library_zone: Mapped[str|None]=mapped_column(String(80)); kiosk_identifier: Mapped[str|None]=mapped_column(String(80), unique=True)


class UserSession(UUIDPK, TimestampMixin, Base):
    __tablename__="user_sessions"; __table_args__=(CheckConstraint("ended_at IS NULL OR ended_at >= started_at"), CheckConstraint("duration_seconds IS NULL OR duration_seconds >= 0"), Index("ix_session_user_started","user_id","started_at"),)
    user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL"), index=True); channel: Mapped[SessionChannel]=enum_col(SessionChannel); started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True); ended_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); duration_seconds: Mapped[int|None]=mapped_column(Integer); entry_method: Mapped[str|None]=mapped_column(String(50)); identified: Mapped[bool]=mapped_column(Boolean, default=False); exit_reason: Mapped[SessionExitReason|None]=enum_col(SessionExitReason, nullable=True)
    user: Mapped[User|None]=relationship(back_populates="sessions"); events: Mapped[list[InteractionEvent]]=relationship(back_populates="session")


class AuthenticationEvent(UUIDPK, TimestampMixin, Base):
    __tablename__="authentication_events"; __table_args__=(CheckConstraint("confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)"), CheckConstraint("processing_time_ms IS NULL OR processing_time_ms >= 0"), CheckConstraint("attempt_number > 0"), Index("ix_auth_session_time","session_id","occurred_at"),)
    user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL"), index=True); authentication_method: Mapped[AuthenticationMethod]=enum_col(AuthenticationMethod); result: Mapped[AuthenticationResult]=enum_col(AuthenticationResult, index=True); confidence_score: Mapped[float|None]=mapped_column(Float); processing_time_ms: Mapped[int|None]=mapped_column(Integer); attempt_number: Mapped[int]=mapped_column(Integer, default=1); failure_reason: Mapped[str|None]=mapped_column(String(255)); occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class InteractionEvent(UUIDPK, Base):
    __tablename__="interaction_events"; __table_args__=(CheckConstraint("processing_time_ms IS NULL OR processing_time_ms >= 0"), Index("ix_event_session_time","session_id","event_timestamp"), Index("ix_event_type_time","event_type","event_timestamp"),)
    session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL"), index=True); event_type: Mapped[str]=mapped_column(String(100), index=True); event_timestamp: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True); screen_name: Mapped[str|None]=mapped_column(String(100)); input_method: Mapped[InputMethod|None]=enum_col(InputMethod, nullable=True); entity_type: Mapped[str|None]=mapped_column(String(80)); entity_id: Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True)); processing_time_ms: Mapped[int|None]=mapped_column(Integer); success: Mapped[bool|None]=mapped_column(Boolean); error_code: Mapped[str|None]=mapped_column(String(80)); event_data: Mapped[dict[str,Any]|None]=mapped_column(JSONB); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    session: Mapped[UserSession]=relationship(back_populates="events")


class Publisher(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="publishers"; name: Mapped[str]=mapped_column(String(255), unique=True)
class Author(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="authors"; name: Mapped[str]=mapped_column(String(255), index=True); biography: Mapped[str|None]=mapped_column(Text)
class Genre(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="genres"; name: Mapped[str]=mapped_column(String(100), unique=True)
class Book(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="books"; __table_args__=(CheckConstraint("publication_year IS NULL OR publication_year BETWEEN 1000 AND 3000"),)
    isbn: Mapped[str|None]=mapped_column(String(20), unique=True); title: Mapped[str]=mapped_column(String(500), index=True); subtitle: Mapped[str|None]=mapped_column(String(500)); description: Mapped[str|None]=mapped_column(Text); publication_year: Mapped[int|None]=mapped_column(Integer); language: Mapped[str]=mapped_column(String(10), default="vi"); publisher_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("publishers.id", ondelete="SET NULL")); cover_url: Mapped[str|None]=mapped_column(String(1000)); book_metadata: Mapped[dict[str,Any]|None]=mapped_column("metadata",JSONB)
    authors: Mapped[list[Author]]=relationship(secondary="book_authors"); genres: Mapped[list[Genre]]=relationship(secondary="book_genres"); copies: Mapped[list[BookCopy]]=relationship(back_populates="book")
class BookAuthor(Base):
    __tablename__="book_authors"; book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="CASCADE"), primary_key=True); author_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True); author_order: Mapped[int]=mapped_column(Integer, default=1); __table_args__=(CheckConstraint("author_order > 0"),)
class BookGenre(Base):
    __tablename__="book_genres"; book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="CASCADE"), primary_key=True); genre_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
class UserFavoriteGenre(Base):
    __tablename__="user_favorite_genres"; user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True); genre_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
class Shelf(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="shelves"; location_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("library_locations.id", ondelete="RESTRICT")); shelf_code: Mapped[str]=mapped_column(String(80), unique=True); floor: Mapped[str|None]=mapped_column(String(30)); zone: Mapped[str|None]=mapped_column(String(80)); row: Mapped[str|None]=mapped_column(String(30)); column: Mapped[str|None]=mapped_column(String(30)); map_reference: Mapped[str|None]=mapped_column(String(255))
class BookCopy(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="book_copies"; book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), index=True); barcode: Mapped[str]=mapped_column(String(100), unique=True); status: Mapped[CopyStatus]=enum_col(CopyStatus, index=True); shelf_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("shelves.id", ondelete="SET NULL")); acquisition_date: Mapped[date|None]=mapped_column(Date); condition: Mapped[str|None]=mapped_column(String(80)); book: Mapped[Book]=relationship(back_populates="copies")
class Ebook(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="ebooks"; book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), index=True); source: Mapped[str]=mapped_column(String(100)); access_url: Mapped[str]=mapped_column(String(1000)); access_type: Mapped[str]=mapped_column(String(50)); availability: Mapped[bool]=mapped_column(Boolean, default=True); __table_args__=(UniqueConstraint("book_id","source","access_url"),)


class SearchQuery(UUIDPK, TimestampMixin, Base):
    __tablename__="search_queries"; __table_args__=(CheckConstraint("processing_time_ms IS NULL OR processing_time_ms >= 0"), CheckConstraint("result_count >= 0"), Index("ix_search_session_time","session_id","query_timestamp"),)
    session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); query_text: Mapped[str]=mapped_column(Text); normalized_query: Mapped[str|None]=mapped_column(Text); input_method: Mapped[InputMethod]=enum_col(InputMethod, index=True); search_type: Mapped[SearchType]=enum_col(SearchType); author_requested: Mapped[str|None]=mapped_column(String(255)); genre_requested: Mapped[str|None]=mapped_column(String(100)); title_requested: Mapped[str|None]=mapped_column(String(500)); keywords: Mapped[list[str]|None]=mapped_column(JSONB); quote_text: Mapped[str|None]=mapped_column(Text); query_timestamp: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True); processing_time_ms: Mapped[int|None]=mapped_column(Integer); result_count: Mapped[int]=mapped_column(Integer, default=0); successful_search: Mapped[bool]=mapped_column(Boolean, default=False)
class SearchResult(UUIDPK, TimestampMixin, Base):
    __tablename__="search_results"; __table_args__=(UniqueConstraint("search_query_id","rank_position"), CheckConstraint("rank_position > 0"), CheckConstraint("similarity_score IS NULL OR similarity_score >= 0"), Index("ix_search_result_rank","search_query_id","rank_position"),)
    search_query_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("search_queries.id", ondelete="RESTRICT")); book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), index=True); rank_position: Mapped[int]=mapped_column(Integer); similarity_score: Mapped[float|None]=mapped_column(Float); rag_score: Mapped[float|None]=mapped_column(Float); source_type: Mapped[str]=mapped_column(String(50)); clicked: Mapped[bool]=mapped_column(Boolean, default=False); selected: Mapped[bool]=mapped_column(Boolean, default=False); clicked_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); selected_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))


class AIRequest(UUIDPK, TimestampMixin, Base):
    __tablename__="ai_requests"; __table_args__=(CheckConstraint("latency_ms IS NULL OR latency_ms >= 0"), CheckConstraint("input_tokens >= 0 AND output_tokens >= 0 AND total_tokens >= 0"), CheckConstraint("estimated_cost >= 0"), CheckConstraint("retry_count >= 0"), Index("ix_ai_feature_time","feature_type","request_timestamp"),)
    session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); ai_model_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("ai_models.id", ondelete="RESTRICT"), index=True); prompt_template_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("prompt_templates.id", ondelete="RESTRICT"), index=True); feature_type: Mapped[AIFeatureType]=enum_col(AIFeatureType, index=True); provider: Mapped[str]=mapped_column(String(80)); model_name: Mapped[str]=mapped_column(String(100)); model_version: Mapped[str|None]=mapped_column(String(80)); prompt_version: Mapped[str|None]=mapped_column(String(80)); request_timestamp: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now()); response_timestamp: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); latency_ms: Mapped[int|None]=mapped_column(Integer); input_tokens: Mapped[int]=mapped_column(Integer, default=0); output_tokens: Mapped[int]=mapped_column(Integer, default=0); total_tokens: Mapped[int]=mapped_column(Integer, default=0); estimated_cost: Mapped[Decimal]=mapped_column(Numeric(14,6), default=0); currency: Mapped[str]=mapped_column(String(3), default="USD"); status: Mapped[AIRequestStatus]=enum_col(AIRequestStatus, index=True); error_code: Mapped[str|None]=mapped_column(String(80)); retry_count: Mapped[int]=mapped_column(Integer, default=0)
class AIRequestContent(UUIDPK, TimestampMixin, Base):
    __tablename__="ai_request_contents"; __table_args__=(UniqueConstraint("ai_request_id"),)
    ai_request_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("ai_requests.id", ondelete="RESTRICT")); redacted_prompt: Mapped[str|None]=mapped_column(Text); redacted_response: Mapped[str|None]=mapped_column(Text); encrypted_payload_reference: Mapped[str|None]=mapped_column(String(500)); redaction_version: Mapped[str]=mapped_column(String(50)); retention_until: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class RAGRequest(UUIDPK, TimestampMixin, Base):
    __tablename__="rag_requests"; __table_args__=(CheckConstraint("retrieval_time_ms IS NULL OR retrieval_time_ms >= 0"), CheckConstraint("generation_time_ms IS NULL OR generation_time_ms >= 0"), CheckConstraint("total_time_ms IS NULL OR total_time_ms >= 0"), CheckConstraint("retrieved_document_count >= 0"),)
    ai_request_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("ai_requests.id", ondelete="RESTRICT"), unique=True); search_query_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("search_queries.id", ondelete="RESTRICT")); embedding_model: Mapped[str]=mapped_column(String(120)); retrieval_started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); retrieval_completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); retrieval_time_ms: Mapped[int|None]=mapped_column(Integer); generation_time_ms: Mapped[int|None]=mapped_column(Integer); total_time_ms: Mapped[int|None]=mapped_column(Integer); retrieved_document_count: Mapped[int]=mapped_column(Integer, default=0)
class Document(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="documents"; book_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("books.id", ondelete="SET NULL")); source_type: Mapped[str]=mapped_column(String(50)); source_reference: Mapped[str]=mapped_column(String(1000)); title: Mapped[str|None]=mapped_column(String(500)); content_hash: Mapped[str]=mapped_column(String(64), unique=True)
class DocumentChunk(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="document_chunks"; __table_args__=(UniqueConstraint("document_id","chunk_index"), CheckConstraint("chunk_index >= 0"),)
    document_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("documents.id", ondelete="CASCADE")); chunk_index: Mapped[int]=mapped_column(Integer); text_content: Mapped[str]=mapped_column(Text); token_count: Mapped[int|None]=mapped_column(Integer); embedding_reference: Mapped[str|None]=mapped_column(String(500)); embedding_model: Mapped[str|None]=mapped_column(String(120))
class RAGRetrievedItem(UUIDPK, TimestampMixin, Base):
    __tablename__="rag_retrieved_items"; __table_args__=(UniqueConstraint("rag_request_id","rank_position"), CheckConstraint("rank_position > 0"), Index("ix_rag_item_rank","rag_request_id","rank_position"),)
    rag_request_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("rag_requests.id", ondelete="RESTRICT")); book_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("books.id", ondelete="RESTRICT")); document_chunk_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("document_chunks.id", ondelete="RESTRICT")); rank_position: Mapped[int]=mapped_column(Integer); similarity_score: Mapped[float]=mapped_column(Float); source_type: Mapped[str]=mapped_column(String(50)); selected_for_context: Mapped[bool]=mapped_column(Boolean, default=False); relevance_label: Mapped[bool|None]=mapped_column(Boolean)


class RecommendationRun(UUIDPK, TimestampMixin, Base):
    __tablename__="recommendation_runs"; __table_args__=(CheckConstraint("processing_time_ms IS NULL OR processing_time_ms >= 0"),)
    session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); trigger_type: Mapped[RecommendationTrigger]=enum_col(RecommendationTrigger); algorithm: Mapped[str]=mapped_column(String(100)); model_name: Mapped[str|None]=mapped_column(String(100)); model_version: Mapped[str|None]=mapped_column(String(80)); prompt_version: Mapped[str|None]=mapped_column(String(80)); processing_time_ms: Mapped[int|None]=mapped_column(Integer); ai_request_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("ai_requests.id", ondelete="RESTRICT"))
class RecommendationItem(UUIDPK, TimestampMixin, Base):
    __tablename__="recommendation_items"; __table_args__=(UniqueConstraint("recommendation_run_id","rank_position"), CheckConstraint("rank_position > 0"), CheckConstraint("feedback_score IS NULL OR feedback_score BETWEEN 1 AND 5"), Index("ix_recommendation_item_rank","recommendation_run_id","rank_position"),)
    recommendation_run_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("recommendation_runs.id", ondelete="RESTRICT")); book_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), index=True); rank_position: Mapped[int]=mapped_column(Integer); ai_score: Mapped[float|None]=mapped_column(Float); recommendation_reason: Mapped[str|None]=mapped_column(Text); shown_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); clicked_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); saved_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); borrowed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); feedback_score: Mapped[int|None]=mapped_column(Integer)
Recommendation = RecommendationItem


class GameSession(UUIDPK, TimestampMixin, Base):
    __tablename__="game_sessions"; __table_args__=(CheckConstraint("ended_at IS NULL OR ended_at >= started_at"), CheckConstraint("score >= 0"), CheckConstraint("question_count >= 0 AND correct_count >= 0 AND correct_count <= question_count"),)
    user_session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), index=True); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); ended_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); topic: Mapped[str|None]=mapped_column(String(150)); difficulty: Mapped[str|None]=mapped_column(String(50)); score: Mapped[int]=mapped_column(Integer, default=0); question_count: Mapped[int]=mapped_column(Integer, default=0); correct_count: Mapped[int]=mapped_column(Integer, default=0); completion_status: Mapped[GameCompletionStatus]=enum_col(GameCompletionStatus)
class GameQuestion(UUIDPK, TimestampMixin, Base):
    __tablename__="game_questions"; game_session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("game_sessions.id", ondelete="RESTRICT")); question_text: Mapped[str]=mapped_column(Text); topic: Mapped[str|None]=mapped_column(String(150)); difficulty: Mapped[str|None]=mapped_column(String(50)); generated_by_ai: Mapped[bool]=mapped_column(Boolean, default=False); ai_request_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("ai_requests.id", ondelete="RESTRICT")); correct_answer_hash: Mapped[str]=mapped_column(String(255)); ordering: Mapped[int]=mapped_column(Integer); __table_args__=(UniqueConstraint("game_session_id","ordering"), CheckConstraint("ordering > 0"),)
class GameAnswer(UUIDPK, TimestampMixin, Base):
    __tablename__="game_answers"; __table_args__=(CheckConstraint("response_time_ms >= 0"),)
    question_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("game_questions.id", ondelete="RESTRICT")); user_answer: Mapped[str|None]=mapped_column(Text); is_correct: Mapped[bool]=mapped_column(Boolean); response_time_ms: Mapped[int]=mapped_column(Integer); answered_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))


class BorrowingRecord(UUIDPK, TimestampMixin, Base):
    __tablename__="borrowing_records"; __table_args__=(CheckConstraint("due_at >= borrowed_at"), CheckConstraint("returned_at IS NULL OR returned_at >= borrowed_at"), CheckConstraint("renewal_count >= 0"), Index("ix_borrow_user_status","user_id","status"), Index("ix_borrow_book_time","book_copy_id","borrowed_at"),)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True); book_copy_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("book_copies.id", ondelete="RESTRICT"), index=True); session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT")); borrowed_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), index=True); due_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); returned_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True), index=True); borrow_channel: Mapped[SessionChannel]=enum_col(SessionChannel); authentication_method: Mapped[AuthenticationMethod]=enum_col(AuthenticationMethod); renewal_count: Mapped[int]=mapped_column(Integer, default=0); status: Mapped[BorrowingStatus]=enum_col(BorrowingStatus, index=True); source_search_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("search_queries.id", ondelete="RESTRICT")); source_recommendation_item_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("recommendation_items.id", ondelete="RESTRICT")); attribution_source: Mapped[str]=mapped_column(String(40), default="DIRECT")
    user: Mapped[User]=relationship(back_populates="borrowings")
class ReturnEvent(UUIDPK, TimestampMixin, Base):
    __tablename__="return_events"; borrowing_record_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("borrowing_records.id", ondelete="RESTRICT")); occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL")); condition: Mapped[str|None]=mapped_column(String(80)); processing_time_ms: Mapped[int|None]=mapped_column(Integer); __table_args__=(CheckConstraint("processing_time_ms IS NULL OR processing_time_ms >= 0"),)
class EbookAccessEvent(UUIDPK, TimestampMixin, Base):
    __tablename__="ebook_access_events"; ebook_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("ebooks.id", ondelete="RESTRICT")); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); session_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT")); accessed_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); access_outcome: Mapped[str]=mapped_column(String(40))


class Notification(UUIDPK, TimestampMixin, Base):
    __tablename__="notifications"; user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True); borrowing_record_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("borrowing_records.id", ondelete="RESTRICT")); notification_type: Mapped[str]=mapped_column(String(80)); scheduled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), index=True); sent_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); delivery_channel: Mapped[str]=mapped_column(String(40)); delivery_status: Mapped[NotificationStatus]=enum_col(NotificationStatus, index=True); opened_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); failure_reason: Mapped[str|None]=mapped_column(String(255))
class ReturnReminder(UUIDPK, TimestampMixin, Base):
    __tablename__="return_reminders"; notification_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("notifications.id", ondelete="RESTRICT"), unique=True); borrowing_record_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("borrowing_records.id", ondelete="RESTRICT")); reminder_sequence: Mapped[int]=mapped_column(Integer); days_relative_to_due: Mapped[int]=mapped_column(Integer); __table_args__=(UniqueConstraint("borrowing_record_id","reminder_sequence"), CheckConstraint("reminder_sequence > 0"),)

class Survey(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="surveys"; title: Mapped[str]=mapped_column(String(255)); survey_version: Mapped[str]=mapped_column(String(30)); active: Mapped[bool]=mapped_column(Boolean, default=True); __table_args__=(UniqueConstraint("title","survey_version"),)
class SurveyQuestion(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="survey_questions"; survey_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("surveys.id", ondelete="RESTRICT")); question_code: Mapped[str]=mapped_column(String(80)); question_text: Mapped[str]=mapped_column(Text); question_type: Mapped[QuestionType]=enum_col(QuestionType); ordering: Mapped[int]=mapped_column(Integer); required: Mapped[bool]=mapped_column(Boolean, default=False); options: Mapped[list[Any]|None]=mapped_column(JSONB); scale_min: Mapped[int|None]=mapped_column(Integer); scale_max: Mapped[int|None]=mapped_column(Integer); construct_name: Mapped[str|None]=mapped_column(String(100)); __table_args__=(UniqueConstraint("survey_id","question_code"), UniqueConstraint("survey_id","ordering"), CheckConstraint("ordering > 0"), CheckConstraint("scale_min IS NULL OR scale_max IS NULL OR scale_max >= scale_min"),)
class SurveyResponse(UUIDPK, TimestampMixin, Base):
    __tablename__="survey_responses"; survey_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("surveys.id", ondelete="RESTRICT")); session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT")); user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); anonymous_participant_code: Mapped[str|None]=mapped_column(String(64), index=True); started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); submitted_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); __table_args__=(CheckConstraint("submitted_at IS NULL OR submitted_at >= started_at"),)
class SurveyAnswer(UUIDPK, TimestampMixin, Base):
    __tablename__="survey_answers"; response_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("survey_responses.id", ondelete="RESTRICT")); question_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("survey_questions.id", ondelete="RESTRICT")); numeric_value: Mapped[Decimal|None]=mapped_column(Numeric(10,2)); text_value: Mapped[str|None]=mapped_column(Text); option_value: Mapped[str|None]=mapped_column(String(255)); boolean_value: Mapped[bool|None]=mapped_column(Boolean); __table_args__=(UniqueConstraint("response_id","question_id"),)

class ResearchStudy(UUIDPK, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="research_studies"; title: Mapped[str]=mapped_column(String(300)); research_question: Mapped[str]=mapped_column(Text); hypothesis: Mapped[str|None]=mapped_column(Text); version: Mapped[str]=mapped_column(String(30)); start_date: Mapped[date|None]=mapped_column(Date); end_date: Mapped[date|None]=mapped_column(Date); status: Mapped[ResearchStudyStatus]=enum_col(ResearchStudyStatus); __table_args__=(UniqueConstraint("title","version"), CheckConstraint("end_date IS NULL OR start_date IS NULL OR end_date >= start_date"),)
class ExperimentGroup(UUIDPK, TimestampMixin, Base):
    __tablename__="experiment_groups"; research_study_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("research_studies.id", ondelete="RESTRICT")); name: Mapped[str]=mapped_column(String(100)); description: Mapped[str|None]=mapped_column(Text); __table_args__=(UniqueConstraint("research_study_id","name"),)
class ResearchParticipant(UUIDPK, TimestampMixin, Base):
    __tablename__="research_participants"; research_study_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("research_studies.id", ondelete="RESTRICT")); anonymous_participant_code: Mapped[str]=mapped_column(String(64)); linked_user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL")); consent_record_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("consent_records.id", ondelete="RESTRICT")); joined_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); withdrawn_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); __table_args__=(UniqueConstraint("research_study_id","anonymous_participant_code"), CheckConstraint("withdrawn_at IS NULL OR withdrawn_at >= joined_at"),)
class ParticipantAssignment(UUIDPK, TimestampMixin, Base):
    __tablename__="participant_assignments"; participant_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("research_participants.id", ondelete="RESTRICT")); experiment_group_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("experiment_groups.id", ondelete="RESTRICT")); assigned_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); ended_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); assignment_reason: Mapped[str|None]=mapped_column(String(255)); __table_args__=(UniqueConstraint("participant_id","experiment_group_id","assigned_at"), CheckConstraint("ended_at IS NULL OR ended_at >= assigned_at"),)

class SystemPerformanceLog(UUIDPK, Base):
    __tablename__="system_performance_logs"; __table_args__=(CheckConstraint("response_time_ms >= 0"), CheckConstraint("database_time_ms IS NULL OR database_time_ms >= 0"), CheckConstraint("ai_time_ms IS NULL OR ai_time_ms >= 0"), CheckConstraint("network_latency_ms IS NULL OR network_latency_ms >= 0"), Index("ix_performance_service_time","service","timestamp"),)
    timestamp: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True); service: Mapped[str]=mapped_column(String(100)); endpoint: Mapped[str|None]=mapped_column(String(500)); request_type: Mapped[str|None]=mapped_column(String(20)); response_time_ms: Mapped[int]=mapped_column(Integer); database_time_ms: Mapped[int|None]=mapped_column(Integer); ai_time_ms: Mapped[int|None]=mapped_column(Integer); network_latency_ms: Mapped[int|None]=mapped_column(Integer); status_code: Mapped[int|None]=mapped_column(Integer); cpu_usage: Mapped[float|None]=mapped_column(Float); memory_usage: Mapped[float|None]=mapped_column(Float); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL")); session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT")); request_id: Mapped[str|None]=mapped_column(String(100))
class SystemError(UUIDPK, TimestampMixin, Base):
    __tablename__="system_errors"; session_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT")); device_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("devices.id", ondelete="SET NULL")); component: Mapped[str]=mapped_column(String(100), index=True); error_code: Mapped[str]=mapped_column(String(80), index=True); error_message: Mapped[str]=mapped_column(Text); severity: Mapped[str]=mapped_column(String(20), index=True); occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), index=True); resolved_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); __table_args__=(CheckConstraint("resolved_at IS NULL OR resolved_at >= occurred_at"),)
class AuditLog(UUIDPK, Base):
    __tablename__="audit_logs"; __table_args__=(Index("ix_audit_target_time","target_type","target_id","timestamp"),)
    actor_user_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True); action: Mapped[str]=mapped_column(String(100), index=True); target_type: Mapped[str]=mapped_column(String(80)); target_id: Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True)); timestamp: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), index=True); ip_address: Mapped[str|None]=mapped_column(INET); details: Mapped[dict[str,Any]|None]=mapped_column(JSONB); request_id: Mapped[str|None]=mapped_column(String(100), index=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())

UserInteraction = InteractionEvent
