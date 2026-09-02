from fastapi import APIRouter

from app.api.v1.routes import (
    ai,
    book_suggestions,
    conversations,
    face_authentication,
    interactions,
    knowledge,
    prompts,
    reports,
    sessions,
    surveys,
    users,
)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(face_authentication.router, prefix="/face-authentication", tags=["face-authentication"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(book_suggestions.router, prefix="/book-suggestions", tags=["book-suggestions"])
api_router.include_router(surveys.router, prefix="/surveys", tags=["surveys"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
