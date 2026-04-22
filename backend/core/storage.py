"""Image storage providers and factory for pluggable backends."""
import asyncio
import os
import uuid
from functools import lru_cache
from io import BytesIO
from typing import Any, Protocol

import cloudinary
import cloudinary.uploader
from fastapi import HTTPException
from PIL import Image

from config import settings

_MEDIA_DIR = os.getenv("MEDIA_DIR", "/app/media")


class StorageProvider(Protocol):
    async def upload_image_variants(self, file_name: str, raw: bytes, owner_key: str) -> dict[str, Any]:
        ...


class CloudinaryStorageProvider:
    def __init__(self) -> None:
        if not settings.cloudinary_cloud_name or not settings.cloudinary_api_key or not settings.cloudinary_api_secret:
            raise HTTPException(status_code=500, detail="Missing Cloudinary configuration")
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
        )

    def _upload_variants_sync(self, file_name: str, raw: bytes, owner_key: str) -> dict[str, Any]:
        image = Image.open(BytesIO(raw))

        web = image.copy()
        web.thumbnail((1300, 720))
        web_buf = BytesIO()
        web.save(web_buf, format="JPEG")
        web_buf.seek(0)

        mob = image.copy()
        mob.thumbnail((360, 720))
        mob_buf = BytesIO()
        mob.save(mob_buf, format="JPEG")
        mob_buf.seek(0)

        web_res = cloudinary.uploader.upload(
            web_buf,
            public_id=f"{owner_key}/web_{file_name}",
            folder="giveandtake",
            resource_type="image",
        )
        mob_res = cloudinary.uploader.upload(
            mob_buf,
            public_id=f"{owner_key}/mob_{file_name}",
            folder="giveandtake",
            resource_type="image",
        )

        return {
            "key": owner_key,
            "name": file_name,
            "web_url": web_res.get("secure_url"),
            "mob_url": mob_res.get("secure_url"),
        }

    async def upload_image_variants(self, file_name: str, raw: bytes, owner_key: str) -> dict[str, Any]:
        return await asyncio.to_thread(self._upload_variants_sync, file_name, raw, owner_key)


class NotImplementedStorageProvider:
    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    async def upload_image_variants(self, file_name: str, raw: bytes, owner_key: str) -> dict[str, Any]:
        raise HTTPException(status_code=501, detail=f"Storage backend '{self.storage_name}' is not implemented")


class LocalStorageProvider:
    """Saves web + mobile variants to local disk under MEDIA_DIR and returns /media/... URLs."""

    def _save_variant(self, image: Image.Image, max_size: tuple[int, int], dest_path: str) -> None:
        variant = image.copy()
        variant.thumbnail(max_size)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        variant.save(dest_path, format="JPEG")

    async def upload_image_variants(self, file_name: str, raw: bytes, owner_key: str) -> dict[str, Any]:
        base_name = f"{uuid.uuid4().hex}_{os.path.splitext(file_name)[0]}.jpg"
        web_name = f"web_{base_name}"
        mob_name = f"mob_{base_name}"
        sub_dir = os.path.join(_MEDIA_DIR, owner_key)

        image = Image.open(BytesIO(raw))

        await asyncio.to_thread(self._save_variant, image, (1300, 720), os.path.join(sub_dir, web_name))
        await asyncio.to_thread(self._save_variant, image, (360, 720), os.path.join(sub_dir, mob_name))

        return {
            "key": owner_key,
            "name": file_name,
            "web_url": f"/media/{owner_key}/{web_name}",
            "mob_url": f"/media/{owner_key}/{mob_name}",
        }


@lru_cache
def get_storage_provider() -> StorageProvider:
    storage_type = settings.storage_type
    if storage_type == "cloudinary":
        return CloudinaryStorageProvider()
    if storage_type in {"azure", "azure_blob"}:
        return NotImplementedStorageProvider("azure")
    if storage_type in {"google", "google_drive", "gdrive"}:
        return NotImplementedStorageProvider("google_drive")
    if storage_type in {"local"}:
        return LocalStorageProvider()
    raise HTTPException(status_code=500, detail=f"Unsupported storage type: {storage_type}")
