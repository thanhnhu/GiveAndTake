import uuid
from typing import Any

import psycopg

from core.security import can_edit, next_number
from core.utils import dt, paginate, to_bool, to_int
from schemas.taker import TakerCreate, TakerUpdate


class TakerRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    def _serialize(self, row: tuple, user: dict | None, donates: list | None = None) -> dict[str, Any]:
        owner_id = row[1]
        return {
            "id": str(row[0]),
            "user": owner_id,
            "date_created": dt(row[2]),
            "last_modified": dt(row[3]),
            "number": row[4],
            "name": row[5],
            "address": row[6],
            "phone": row[7],
            "description": row[8],
            "images": row[9],
            "stop_donate": bool(row[10]),
            "city": row[11],
            "can_edit": bool(user and can_edit(owner_id, user)),
            "can_delete": bool(user and user["is_superuser"]),
            "donates": donates or [],
        }

    def _serialize_donate(self, row: tuple) -> dict[str, Any]:
        return {
            "id": str(row[0]),
            "taker": str(row[1]),
            "user": row[2],
            "date_created": dt(row[3]),
            "last_modified": dt(row[4]),
            "donate": row[5],
            "description": row[6],
        }

    async def _fetch_donates(self, taker_ids: list) -> dict[str, list]:
        donates: dict[str, list] = {str(tid): [] for tid in taker_ids}
        if not taker_ids:
            return donates
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, taker_id, user_id, date_created, last_modified, donate, description
                FROM takers_donate WHERE taker_id = ANY(%s) ORDER BY date_created ASC
                """,
                (taker_ids,),
            )
            for d in await cur.fetchall():
                donates[str(d[1])].append(self._serialize_donate(d))
        return donates

    async def list(
        self,
        *,
        user: dict | None,
        page: int,
        page_size: int,
        city: str | None,
        number: str | None,
        name: str | None,
        phone: str | None,
        is_mine: bool,
    ) -> dict[str, Any]:
        sql = [
            """
            SELECT t.id, t.user_id, t.date_created, t.last_modified, t.number,
                   t.name, t.address, t.phone, t.description, t.images,
                   t.stop_donate, t.city_id,
                   COALESCE(d.total, 0) AS total_donates
            FROM takers_taker t
            LEFT JOIN (
                SELECT taker_id, COALESCE(SUM(donate), 0) AS total FROM takers_donate GROUP BY taker_id
            ) d ON d.taker_id = t.id
            """
        ]
        where: list[str] = []
        params: list[Any] = []

        if user:
            if is_mine:
                where.append("t.user_id = %s")
                params.append(user["id"])
            else:
                where.append("(t.user_id = %s OR t.stop_donate = FALSE)")
                params.append(user["id"])
        else:
            where.append("t.stop_donate = FALSE")

        if city and city.strip():
            where.append("t.city_id = %s")
            params.append(city.strip())
        if number and number.strip():
            where.append("CAST(t.number AS TEXT) = %s")
            params.append(number.strip())
        if name and name.strip():
            where.append("t.name ILIKE %s")
            params.append(f"%{name.strip()}%")
        if phone and phone.strip():
            where.append("t.phone LIKE %s")
            params.append(f"%{phone.strip()}%")

        if where:
            sql.append("WHERE " + " AND ".join(where))
        sql.append("ORDER BY total_donates ASC, t.date_created ASC")
        base_query = "\n".join(sql)

        count_query, paged_params = paginate(base_query, params, page, page_size)

        async with self.conn.cursor() as cur:
            await cur.execute(count_query, params)
            count = (await cur.fetchone())[0]
            await cur.execute(base_query + " LIMIT %s OFFSET %s", paged_params)
            rows = await cur.fetchall()

        donates_by_taker = await self._fetch_donates([r[0] for r in rows])
        results = [self._serialize(r, user, donates_by_taker.get(str(r[0]), [])) for r in rows]
        return {"count": count, "results": results}

    async def create(self, user_id: int, data: TakerCreate) -> dict[str, Any]:
        number = data.number or await next_number(self.conn, "takers_taker")
        new_id = str(uuid.uuid4())
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO takers_taker
                    (id, date_created, last_modified, number, name, address, phone,
                     description, images, stop_donate, city_id, user_id)
                VALUES (%s::uuid, NOW(), NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                          description, images, stop_donate, city_id
                """,
                (new_id, number, data.name, data.address, data.phone, data.description,
                 data.images, data.stop_donate, data.city, user_id),
            )
            row = await cur.fetchone()
        await self.conn.commit()
        user_stub = {"id": user_id, "is_staff": True, "is_superuser": False}
        result = self._serialize(row, user_stub)
        result["can_edit"] = True
        result["can_delete"] = False
        return result

    async def get_owner(self, taker_id: str) -> int | None:
        async with self.conn.cursor() as cur:
            await cur.execute("SELECT user_id FROM takers_taker WHERE id = %s::uuid", (taker_id,))
            row = await cur.fetchone()
        return row[0] if row else None

    async def update(self, taker_id: str, data: TakerUpdate, user: dict) -> dict[str, Any] | None:
        field_map = {
            "number": "number", "name": "name", "address": "address",
            "phone": "phone", "description": "description", "images": "images",
            "stop_donate": "stop_donate", "city": "city_id",
        }
        update_fields: list[str] = []
        params: list[Any] = []
        for key in data.model_fields_set:
            if key in field_map:
                update_fields.append(f"{field_map[key]} = %s")
                params.append(getattr(data, key))

        async with self.conn.cursor() as cur:
            if update_fields:
                update_sql = ", ".join(update_fields + ["last_modified = NOW()"])
                await cur.execute(
                    f"""
                    UPDATE takers_taker SET {update_sql} WHERE id = %s::uuid
                    RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                              description, images, stop_donate, city_id
                    """,
                    params + [taker_id],
                )
                await self.conn.commit()
            else:
                await cur.execute(
                    """
                    SELECT id, user_id, date_created, last_modified, number, name, address, phone,
                           description, images, stop_donate, city_id
                    FROM takers_taker WHERE id = %s::uuid
                    """,
                    (taker_id,),
                )
            row = await cur.fetchone()
            if not row:
                return None

            await cur.execute(
                """
                SELECT id, taker_id, user_id, date_created, last_modified, donate, description
                FROM takers_donate WHERE taker_id = %s::uuid ORDER BY date_created ASC
                """,
                (taker_id,),
            )
            donates = [self._serialize_donate(d) for d in await cur.fetchall()]

        return self._serialize(row, user, donates)

    async def delete(self, taker_id: str, user: dict) -> dict[str, Any] | None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM takers_taker WHERE id = %s::uuid
                RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                          description, images, stop_donate, city_id
                """,
                (taker_id,),
            )
            row = await cur.fetchone()
            if not row:
                return None
        await self.conn.commit()
        return {"data": self._serialize(row, user)}

    async def toggle_stop_donate(self, taker_id: str) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                "UPDATE takers_taker SET stop_donate = NOT stop_donate, last_modified = NOW() "
                "WHERE id = %s::uuid",
                (taker_id,),
            )
        await self.conn.commit()
