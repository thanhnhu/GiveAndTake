from typing import Any

from pydantic import BaseModel, ConfigDict


class DonateOut(BaseModel):
    id: str
    taker: str
    user: int
    date_created: str | None = None
    last_modified: str | None = None
    donate: int
    description: str | None = None


class TakerCreate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    images: list[Any] | None = None
    stop_donate: bool = False
    city: int | None = None
    number: int | None = None


class TakerUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    images: list[Any] | None = None
    stop_donate: bool | None = None
    city: int | None = None
    number: int | None = None


class TakerOut(BaseModel):
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
    stop_donate: bool
    city: int | None = None
    can_edit: bool
    can_delete: bool
    donates: list[DonateOut] = []


class PaginatedTakers(BaseModel):
    count: int
    results: list[TakerOut]
