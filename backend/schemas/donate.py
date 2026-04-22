from pydantic import BaseModel, ConfigDict


class DonateCreate(BaseModel):
    taker: str
    donate: int
    description: str | None = None


class DonateUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    taker: str | None = None
    donate: int | None = None
    description: str | None = None


class DonateOut(BaseModel):
    id: str
    taker: str
    user: int
    date_created: str | None = None
    last_modified: str | None = None
    donate: int
    description: str | None = None


class DeletedDonateOut(BaseModel):
    data: DonateOut
