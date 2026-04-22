import uuid
from typing import Any

import psycopg

from core.utils import dt
from schemas.donate import DonateCreate, DonateUpdate


class DonateRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    def _serialize(self, row: tuple) -> dict[str, Any]:
        return {
            "id": str(row[0]),
            "taker": str(row[1]),
            "user": row[2],
            "date_created": dt(row[3]),
            "last_modified": dt(row[4]),
            "donate": row[5],
            "description": row[6],
        }

    async def get_owner(self, donate_id: str) -> int | None:
        async with self.conn.cursor() as cur:
            await cur.execute("SELECT user_id FROM takers_donate WHERE id = %s::uuid", (donate_id,))
            row = await cur.fetchone()
        return row[0] if row else None

    async def create(self, user_id: int, data: DonateCreate) -> dict[str, Any]:
        new_id = str(uuid.uuid4())
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO takers_donate
                    (id, date_created, last_modified, taker_id, user_id, donate, description)
                VALUES (%s::uuid, NOW(), NOW(), %s::uuid, %s, %s, %s)
                RETURNING id, taker_id, user_id, date_created, last_modified, donate, description
                """,
                (new_id, data.taker, user_id, data.donate, data.description),
            )
            row = await cur.fetchone()
        await self.conn.commit()
        return self._serialize(row)

    async def update(self, donate_id: str, data: DonateUpdate) -> dict[str, Any] | None:
        update_fields: list[str] = []
        params: list[Any] = []
        if "taker" in data.model_fields_set:
            update_fields.append("taker_id = %s::uuid")
            params.append(data.taker)
        if "donate" in data.model_fields_set:
            update_fields.append("donate = %s")
            params.append(data.donate)
        if "description" in data.model_fields_set:
            update_fields.append("description = %s")
            params.append(data.description)

        async with self.conn.cursor() as cur:
            if update_fields:
                update_sql = ", ".join(update_fields + ["last_modified = NOW()"])
                await cur.execute(
                    f"""
                    UPDATE takers_donate SET {update_sql} WHERE id = %s::uuid
                    RETURNING id, taker_id, user_id, date_created, last_modified, donate, description
                    """,
                    params + [donate_id],
                )
                await self.conn.commit()
            else:
                await cur.execute(
                    """
                    SELECT id, taker_id, user_id, date_created, last_modified, donate, description
                    FROM takers_donate WHERE id = %s::uuid
                    """,
                    (donate_id,),
                )
            row = await cur.fetchone()
        return self._serialize(row) if row else None

    async def delete(self, donate_id: str) -> dict[str, Any] | None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM takers_donate WHERE id = %s::uuid
                RETURNING id, taker_id, user_id, date_created, last_modified, donate, description
                """,
                (donate_id,),
            )
            row = await cur.fetchone()
            if not row:
                return None
        await self.conn.commit()
        return {"data": self._serialize(row)}
