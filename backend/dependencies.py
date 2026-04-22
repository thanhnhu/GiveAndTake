"""FastAPI dependency functions and their Annotated type aliases."""
from typing import Annotated, Any, AsyncGenerator

import psycopg
from fastapi import Depends, HTTPException, Request

from core.security import fetch_user_by_token, parse_token_auth


async def get_db(request: Request) -> AsyncGenerator[psycopg.AsyncConnection, None]:
    """Yield an async connection from the application-level connection pool."""
    async with request.app.state.pool.connection() as conn:
        yield conn


# Convenient type aliases — use these in route signatures
DBConn = Annotated[psycopg.AsyncConnection, Depends(get_db)]


async def _get_optional_user(
    request: Request, conn: DBConn
) -> dict[str, Any] | None:
    token = parse_token_auth(request)
    return await fetch_user_by_token(conn, token)


async def _get_current_user(
    user: Annotated[dict[str, Any] | None, Depends(_get_optional_user)],
) -> dict[str, Any]:
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication credentials were not provided.",
        )
    return user


# Routes that require authentication
CurrentUser = Annotated[dict[str, Any], Depends(_get_current_user)]

# Routes where auth is optional (e.g. listing takers/givers)
OptionalUser = Annotated[dict[str, Any] | None, Depends(_get_optional_user)]
