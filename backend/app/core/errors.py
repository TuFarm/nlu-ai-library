from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: object = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(SQLAlchemyError)
    async def database_error(_: Request, __: SQLAlchemyError) -> JSONResponse:
        return JSONResponse(status_code=503, content={"success": False,
            "message": "Database operation is unavailable", "error": {"code": "DATABASE_ERROR", "details": None}})

    @app.exception_handler(AppError)
    async def app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"success": False, "message": exc.message,
            "error": {"code": exc.code, "details": exc.details}})

    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "error": {"code": "VALIDATION_ERROR", "details": jsonable_encoder(exc.errors())},
            },
        )
