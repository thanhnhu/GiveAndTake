"""Authentication and authorization helpers (no HTTP concerns)."""
import base64
import hashlib
import secrets
from typing import Any

import psycopg
from fastapi import HTTPException, Request


def parse_token_auth(request: Request) -> str | None:
    auth = request.headers.get("authorization", "")
    if not auth:
        return None
    parts = auth.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "token":
        return None
    return parts[1].strip() or None


async def fetch_user_by_token(
    conn: psycopg.AsyncConnection, token: str | None
) -> dict[str, Any] | None:
    if not token:
        return None
    async with conn.cursor() as cur:
        await cur.execute(
            """
            SELECT u.id, u.is_staff, u.is_superuser
            FROM authtoken_token t
            JOIN auth_user u ON u.id = t.user_id
            WHERE t.key = %s
            """,
            (token,),
        )
        row = await cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "is_staff": bool(row[1]), "is_superuser": bool(row[2])}


async def fetch_user_by_username(
    conn: psycopg.AsyncConnection, username: str
) -> dict[str, Any] | None:
    async with conn.cursor() as cur:
        await cur.execute(
            """
            SELECT id, username, password, email, first_name, last_name, is_staff, is_active
            FROM auth_user WHERE username = %s
            """,
            (username,),
        )
        row = await cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "username": row[1],
        "password": row[2],
        "email": row[3],
        "first_name": row[4],
        "last_name": row[5],
        "is_staff": bool(row[6]),
        "is_active": bool(row[7]),
    }


def verify_django_password(raw_password: str, encoded: str) -> bool:
    if not encoded or encoded.startswith("!"):
        return False
    parts = encoded.split("$", 3)
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
        return False
    try:
        iterations = int(parts[1])
    except ValueError:
        return False
    salt, stored_hash = parts[2], parts[3]
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode(), salt.encode(), iterations)
    computed = base64.b64encode(dk).decode().strip()
    return secrets.compare_digest(computed, stored_hash)


def hash_django_password(raw_password: str, iterations: int = 870_000) -> str:
    salt = secrets.token_hex(6)
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode(), salt.encode(), iterations)
    encoded = base64.b64encode(dk).decode().strip()
    return f"pbkdf2_sha256${iterations}${salt}${encoded}"


async def get_or_create_token(conn: psycopg.AsyncConnection, user_id: int) -> str:
    async with conn.cursor() as cur:
        await cur.execute("SELECT key FROM authtoken_token WHERE user_id = %s", (user_id,))
        row = await cur.fetchone()
        if row:
            return row[0]
        for _ in range(5):
            token_key = secrets.token_hex(20)
            await cur.execute("SELECT 1 FROM authtoken_token WHERE key = %s", (token_key,))
            if await cur.fetchone() is None:
                await cur.execute(
                    "INSERT INTO authtoken_token (key, created, user_id) VALUES (%s, NOW(), %s)",
                    (token_key, user_id),
                )
                await conn.commit()
                return token_key
    raise HTTPException(status_code=500, detail="Failed to generate auth token")


def can_edit(owner_id: int, user: dict[str, Any]) -> bool:
    return bool(user["id"] == owner_id or user["is_staff"])


async def next_number(conn: psycopg.AsyncConnection, table_name: str) -> int:
    async with conn.cursor() as cur:
        await cur.execute(f"SELECT COALESCE(MAX(number), 0) + 1 FROM {table_name}")  # noqa: S608
        row = await cur.fetchone()
    return int(row[0])
