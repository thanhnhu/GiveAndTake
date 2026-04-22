import uuid
from typing import Any

import psycopg

from core.security import can_edit, next_number
from core.utils import dt, paginate, to_bool, to_int
from schemas.giver import GiverCreate, GiverUpdate


class GiverRepository:
    def __init__(self, conn: psycopg.AsyncConnection) -> None:
        self.conn = conn

    def _serialize(self, row: tuple, user: dict | None) -> dict[str, Any]:
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
            "active": bool(row[10]),
            "city": row[11],
            "can_edit": bool(user and can_edit(owner_id, user)),
            "can_delete": bool(user and user["is_superuser"]),
        }

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
            SELECT g.id, g.user_id, g.date_created, g.last_modified, g.number,
                   g.name, g.address, g.phone, g.description, g.images,
                   g.active, g.city_id
            FROM takers_giver g
            """
        ]
        where: list[str] = []
        params: list[Any] = []

        if user:
            if is_mine:
                where.append("g.user_id = %s")
                params.append(user["id"])
            else:
                where.append("(g.user_id = %s OR g.active = TRUE)")
                params.append(user["id"])
        else:
            where.append("g.active = TRUE")

        if city and city.strip():
            where.append("g.city_id = %s")
            params.append(city.strip())
        if number and number.strip():
            where.append("CAST(g.number AS TEXT) = %s")
            params.append(number.strip())
        if name and name.strip():
            where.append("g.name ILIKE %s")
            params.append(f"%{name.strip()}%")
        if phone and phone.strip():
            where.append("g.phone LIKE %s")
            params.append(f"%{phone.strip()}%")

        if where:
            sql.append("WHERE " + " AND ".join(where))
        sql.append("ORDER BY g.date_created DESC")
        base_query = "\n".join(sql)

        count_query, paged_params = paginate(base_query, params, page, page_size)

        async with self.conn.cursor() as cur:
            await cur.execute(count_query, params)
            count = (await cur.fetchone())[0]
            await cur.execute(base_query + " LIMIT %s OFFSET %s", paged_params)
            rows = await cur.fetchall()

        return {"count": count, "results": [self._serialize(r, user) for r in rows]}

    async def create(self, user_id: int, data: GiverCreate) -> dict[str, Any]:
        number = data.number or await next_number(self.conn, "takers_giver")
        new_id = str(uuid.uuid4())
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO takers_giver
                    (id, date_created, last_modified, number, name, address, phone,
                     description, images, active, city_id, user_id)
                VALUES (%s::uuid, NOW(), NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                          description, images, active, city_id
                """,
                (new_id, number, data.name, data.address, data.phone, data.description,
                 data.images, data.active, data.city, user_id),
            )
            row = await cur.fetchone()
        await self.conn.commit()
        user_stub = {"id": user_id, "is_staff": True, "is_superuser": False}
        result = self._serialize(row, user_stub)
        result["can_edit"] = True
        return result

    async def get_owner(self, giver_id: str) -> int | None:
        async with self.conn.cursor() as cur:
            await cur.execute("SELECT user_id FROM takers_giver WHERE id = %s::uuid", (giver_id,))
            row = await cur.fetchone()
        return row[0] if row else None

    async def update(self, giver_id: str, data: GiverUpdate, user: dict) -> dict[str, Any] | None:
        field_map = {
            "number": "number", "name": "name", "address": "address",
            "phone": "phone", "description": "description", "images": "images",
            "active": "active", "city": "city_id",
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
                    UPDATE takers_giver SET {update_sql} WHERE id = %s::uuid
                    RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                              description, images, active, city_id
                    """,
                    params + [giver_id],
                )
                await self.conn.commit()
            else:
                await cur.execute(
                    """
                    SELECT id, user_id, date_created, last_modified, number, name, address, phone,
                           description, images, active, city_id
                    FROM takers_giver WHERE id = %s::uuid
                    """,
                    (giver_id,),
                )
            row = await cur.fetchone()
        return self._serialize(row, user) if row else None

    async def delete(self, giver_id: str, user: dict) -> dict[str, Any] | None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM takers_giver WHERE id = %s::uuid
                RETURNING id, user_id, date_created, last_modified, number, name, address, phone,
                          description, images, active, city_id
                """,
                (giver_id,),
            )
            row = await cur.fetchone()
            if not row:
                return None
        await self.conn.commit()
        return {"data": self._serialize(row, user)}

    async def toggle_active(self, giver_id: str) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                "UPDATE takers_giver SET active = NOT active, last_modified = NOW() WHERE id = %s::uuid",
                (giver_id,),
            )
        await self.conn.commit()
