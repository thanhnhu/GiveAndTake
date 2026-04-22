from typing import Any

from pydantic import BaseModel


class ImageOut(BaseModel):
    key: str
    name: str
    web_url: str | None = None
    mob_url: str | None = None
