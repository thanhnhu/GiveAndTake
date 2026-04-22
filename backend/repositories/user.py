from typing import Any

import psycopg

from core.security import hash_django_password
from core.utils import dt
from schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    def _serialize(self, row: tuple) -> dict[str, Any]:
        return {
            "id": row[0],
            "password": row[1],
            "last_login": dt(row[2]),
            "is_superuser": bool(row[3]),
            "username": row[4],
            "first_name": row[5],
            "last_name": row[6],
            "email": row[7],
            "is_staff": bool(row[8]),
            "is_active": bool(row[9]),
            "date_joined": dt(row[10]),
        }

    async def create(self, data: UserCreate) -> dict[str, Any]:
        hashed = hash_django_password(data.password)
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO auth_user (
                    password, last_login, is_superuser, username, first_name,
                    last_name, email, is_staff, is_active, date_joined
                )
                VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, TRUE, NOW())
                RETURNING id, password, last_login, is_superuser, username, first_name,
                          last_name, email, is_staff, is_active, date_joined
                """,
                (
                    hashed,
                    data.is_superuser,
                    data.username,
                    data.first_name or "",
                    data.last_name or "",
                    data.email or "",
                    data.is_staff,
                ),
            )
            row = await cur.fetchone()
        await self.conn.commit()
        return self._serialize(row)

    async def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, password, last_login, is_superuser, username, first_name,
                       last_name, email, is_staff, is_active, date_joined
                FROM auth_user WHERE id = %s
                """,
                (user_id,),
            )
            row = await cur.fetchone()
        return self._serialize(row) if row else None

    async def update(self, user_id: int, data: UserUpdate) -> dict[str, Any] | None:
        field_map = {
            "username": "username", "first_name": "first_name", "last_name": "last_name",
            "email": "email", "is_staff": "is_staff", "is_superuser": "is_superuser",
            "is_active": "is_active",
        }
        update_fields: list[str] = []
        params: list[Any] = []
        for key in data.model_fields_set:
            if key == "password" and data.password:
                update_fields.append("password = %s")
                params.append(hash_django_password(data.password))
            elif key in field_map:
                update_fields.append(f"{field_map[key]} = %s")
                params.append(getattr(data, key))

        async with self.conn.cursor() as cur:
            await cur.execute("SELECT id FROM auth_user WHERE id = %s", (user_id,))
            if not await cur.fetchone():
                return None
            if update_fields:
                await cur.execute(
                    f"UPDATE auth_user SET {', '.join(update_fields)} WHERE id = %s",
                    params + [user_id],
                )
                await self.conn.commit()
            await cur.execute(
                """
                SELECT id, password, last_login, is_superuser, username, first_name,
                       last_name, email, is_staff, is_active, date_joined
                FROM auth_user WHERE id = %s
                """,
                (user_id,),
            )
            row = await cur.fetchone()
        return self._serialize(row) if row else None
