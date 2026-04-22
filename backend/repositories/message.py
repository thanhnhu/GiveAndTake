from typing import Any

import psycopg

from schemas.message import MessageCreate


class MessageRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    def _serialize(self, row: tuple) -> dict[str, Any]:
        return {"url": f"/api/messages/{row[0]}/", "subject": row[1], "body": row[2], "pk": row[0]}

    async def list_all(self) -> list[dict[str, Any]]:
        async with self.conn.cursor() as cur:
            await cur.execute("SELECT id, subject, body FROM api_message ORDER BY id DESC")
            rows = await cur.fetchall()
        return [self._serialize(r) for r in rows]

    async def create(self, data: MessageCreate) -> dict[str, Any]:
        async with self.conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO api_message (subject, body) VALUES (%s, %s) RETURNING id, subject, body",
                (data.subject, data.body),
            )
            row = await cur.fetchone()
        await self.conn.commit()
        return self._serialize(row)

    async def delete(self, message_id: int) -> bool:
        async with self.conn.cursor() as cur:
            await cur.execute("DELETE FROM api_message WHERE id = %s", (message_id,))
            deleted = cur.rowcount > 0
        if deleted:
            await self.conn.commit()
        return deleted
