import psycopg
from fastapi import APIRouter, HTTPException, Request, Response

from dependencies import CurrentUser, DBConn
from repositories.user import UserRepository
from schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(tags=["Users"])


@router.post("/api/users/", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, conn: DBConn) -> UserOut:
    try:
        return await UserRepository(conn).create(payload)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="A user with that username already exists.")


@router.get("/api/users/{user_id}", response_model=UserOut)
@router.get("/api/users/{user_id}/", response_model=UserOut)
async def get_user(user_id: int, conn: DBConn, auth_user: CurrentUser) -> UserOut:
    if not (auth_user["is_staff"] or auth_user["id"] == user_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    result = await UserRepository(conn).get_by_id(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/api/users/{user_id}", response_model=UserOut)
@router.put("/api/users/{user_id}/", response_model=UserOut)
@router.patch("/api/users/{user_id}", response_model=UserOut)
@router.patch("/api/users/{user_id}/", response_model=UserOut)
async def update_user(user_id: int, payload: UserUpdate, conn: DBConn, auth_user: CurrentUser) -> UserOut:
    if not (auth_user["is_staff"] or auth_user["id"] == user_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        result = await UserRepository(conn).update(user_id, payload)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="A user with that username already exists.")
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.delete("/api/users/{user_id}")
@router.delete("/api/users/{user_id}/")
async def delete_user(user_id: int) -> Response:
    _ = user_id
    raise HTTPException(status_code=405, detail='Method "DELETE" not allowed.')
