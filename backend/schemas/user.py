from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_staff: bool = False
    is_superuser: bool = False


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None


class UserOut(BaseModel):
    id: int
    password: str
    last_login: str | None = None
    is_superuser: bool
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: str | None = None
