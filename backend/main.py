from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from psycopg_pool import AsyncConnectionPool

from api.router import router as api_router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the async DB connection pool for the application lifetime."""
    pool = AsyncConnectionPool(conninfo=settings.db_dsn, min_size=settings.db_pool_min_size, max_size=settings.db_pool_max_size, open=False)
    await pool.open(wait=True)
    app.state.pool = pool
    yield
    await pool.close()


app = FastAPI(
    title="GiveAndTake API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "System", "description": "Health check and API metadata endpoints."},
        {"name": "Auth", "description": "Authentication and token endpoints."},
        {"name": "Cities", "description": "Reference city data."},
        {"name": "Takers", "description": "Taker management and visibility controls."},
        {"name": "Givers", "description": "Giver management and active state controls."},
        {"name": "Donates", "description": "Donation CRUD operations."},
        {"name": "Users", "description": "User registration and profile management."},
        {"name": "Messages", "description": "Public/contact messages."},
        {"name": "Images", "description": "Image upload and image placeholder endpoints."},
    ],
)


@app.get("/health", tags=["System"])
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "fastapi",
    }


# Docs/schema routes MUST be registered before api_router (which contains
# the /api/{path:path} proxy catch-all registered last).
@app.get("/api/schema", tags=["System"])
@app.get("/api/schema/", tags=["System"])
async def api_schema() -> dict[str, Any]:
    return app.openapi()


@app.get("/api/docs", tags=["System"])
@app.get("/api/docs/", tags=["System"])
async def api_docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/schema/", title="GiveAndTake API Docs")


app.include_router(api_router)

import os as _os
_media_dir = _os.getenv("MEDIA_DIR", "/app/media")
_os.makedirs(_media_dir, exist_ok=True)
app.mount("/media", StaticFiles(directory=_media_dir), name="media")
