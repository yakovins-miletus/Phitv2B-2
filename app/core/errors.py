import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger("heimdall")

PROBLEM_MEDIA_TYPE = "application/problem+json"


class Problem(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None


class FieldError(BaseModel):
    field: str
    message: str


class ValidationProblem(Problem):
    errors: list[FieldError] = []


class AppError(Exception):
    status = 500
    title = "Internal error"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail or self.title)
        self.detail = detail


class NotFoundError(AppError):
    status = 404
    title = "Not found"


def _respond(problem: Problem) -> JSONResponse:
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(exclude_none=True),
        media_type=PROBLEM_MEDIA_TYPE,
    )


def _field_path(loc: tuple[int | str, ...]) -> str:
    parts = [str(part) for part in loc if part not in ("body", "query", "path")]
    return ".".join(parts) or "request"


def register_error_handlers(app: FastAPI, *, debug: bool) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return _respond(
            Problem(
                title=exc.title,
                status=exc.status,
                detail=exc.detail,
                instance=request.url.path,
            )
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = [
            FieldError(field=_field_path(tuple(err["loc"])), message=err["msg"])
            for err in exc.errors()
        ]
        return _respond(
            ValidationProblem(
                title="Validation failed",
                status=422,
                detail="One or more fields are invalid.",
                instance=request.url.path,
                errors=errors,
            )
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s", request.url.path)
        return _respond(
            Problem(
                title="Internal error",
                status=500,
                detail=str(exc) if debug else None,
                instance=request.url.path,
            )
        )
