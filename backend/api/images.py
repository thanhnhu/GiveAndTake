from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from psycopg.types.json import Jsonb

from core.storage import get_storage_provider
from core.utils import to_bool
from dependencies import CurrentUser, DBConn
from schemas.image import ImageOut

router = APIRouter(tags=["Images"])

_SUPPORTED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif"}


@router.post("/api/images/", response_model=list[ImageOut])
async def upload_images(
    conn: DBConn,
    user: CurrentUser,
    files: list[UploadFile] = File(...),
    id: str | None = Form(default=None),
    isTaker: str | None = Form(default=None),
    isGiver: str | None = Form(default=None),
) -> list[ImageOut]:
    storage_provider = get_storage_provider()

    owner_key = (id or "").strip()
    result: list[dict[str, Any]] = []

    for file in files:
        if file.content_type not in _SUPPORTED_TYPES:
            raise HTTPException(status_code=400, detail={"error": "100", "message": "Need images file"})
        raw = await file.read()
        if len(raw) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail={"error": "101", "message": "File size > 10MB"})

        uploaded = await storage_provider.upload_image_variants(file.filename or "image.jpg", raw, owner_key or "tmp")
        if not owner_key:
            uploaded["key"] = ""
        result.append(uploaded)

    link_to_taker = to_bool(isTaker, False)
    link_to_giver = to_bool(isGiver, False)
    if owner_key and result and (link_to_taker or link_to_giver):
        async with conn.cursor() as cur:
            if link_to_taker:
                await cur.execute("SELECT images FROM takers_taker WHERE id = %s::uuid", (owner_key,))
                row = await cur.fetchone()
                if row:
                    await cur.execute(
                        "UPDATE takers_taker SET images = %s, last_modified = NOW() WHERE id = %s::uuid",
                        (Jsonb((row[0] or []) + result), owner_key),
                    )
            elif link_to_giver:
                await cur.execute("SELECT images FROM takers_giver WHERE id = %s::uuid", (owner_key,))
                row = await cur.fetchone()
                if row:
                    await cur.execute(
                        "UPDATE takers_giver SET images = %s, last_modified = NOW() WHERE id = %s::uuid",
                        (Jsonb((row[0] or []) + result), owner_key),
                    )
        await conn.commit()

    return result


@router.get("/api/images/")
async def list_images() -> list:
    return []


@router.get("/api/images/{image_id}")
@router.get("/api/images/{image_id}/")
async def get_image(image_id: str) -> dict[str, Any]:
    return {image_id: image_id, "abc": "abc"}
