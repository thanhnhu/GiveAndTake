from pydantic import BaseModel


class MessageCreate(BaseModel):
    subject: str | None = None
    body: str | None = None


class MessageOut(BaseModel):
    url: str
    subject: str | None = None
    body: str | None = None
    pk: int
