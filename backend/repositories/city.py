from typing import Any

import psycopg


class CityRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    async def list_all(self) -> list[dict[str, Any]]:
        async with self.conn.cursor() as cur:
            await cur.execute("SELECT id, name FROM takers_city ORDER BY id ASC")
            rows = await cur.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]
