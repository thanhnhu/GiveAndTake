from typing import Any

from pydantic import BaseModel, ConfigDict


class GiverCreate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    images: list[Any] | None = None
    active: bool = True
    city: int | None = None
    number: int | None = None


class GiverUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    images: list[Any] | None = None
    active: bool | None = None
    city: int | None = None
    number: int | None = None


class GiverOut(BaseModel):
    id: str
    user: int
    date_created: str | None = None
    last_modified: str | None = None
    number: int
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    images: list[Any] | None = None
    active: bool
    city: int | None = None
    can_edit: bool
    can_delete: bool


class PaginatedGivers(BaseModel):
    count: int
    results: list[GiverOut]
