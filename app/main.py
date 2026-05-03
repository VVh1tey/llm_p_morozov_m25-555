from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import routes_auth, routes_chat
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

    app.include_router(routes_auth.router)
    app.include_router(routes_chat.router)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "environment": settings.ENV}

    return app


app = create_app()
