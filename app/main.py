from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.routing import APIRoute

from app.api import api_router
from app.core.config import settings
from app.core.errors import register_error_handlers
from app.db.seed import init_db, seed_blog_if_empty, seed_if_empty
from app.db.session import async_session_factory, engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_db(engine)
    if settings.seed_on_startup:
        async with async_session_factory() as session:
            await seed_if_empty(session)
            await seed_blog_if_empty(session)
    yield
    await engine.dispose()


def operation_id_from_route_name(route: APIRoute) -> str:
    return route.name


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
        generate_unique_id_function=operation_id_from_route_name,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )
    register_error_handlers(app, debug=settings.debug)
    app.include_router(api_router)
    return app


app = create_app()


@app.get("/health", include_in_schema=False)
async def health_check() -> Response:
    return Response(content="ok", media_type="text/plain")
