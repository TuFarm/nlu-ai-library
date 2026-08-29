from fastapi import APIRouter

from app.api.v1.routes import books, borrowings, interactions, recommendations, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(borrowings.router, prefix="/borrowings", tags=["borrowings"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

