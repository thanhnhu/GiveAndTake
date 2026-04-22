import json

from fastapi import APIRouter, HTTPException

from core.security import fetch_user_by_username, get_or_create_token, verify_django_password
from dependencies import DBConn
from schemas.auth import LoginRequest, LoginResponse

router = APIRouter(tags=["Auth"])


@router.post("/api/auth/", response_model=LoginResponse)
async def login(payload: LoginRequest, conn: DBConn) -> LoginResponse:
    user = await fetch_user_by_username(conn, payload.username.strip())
    if not user or not user["is_active"] or not verify_django_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Unable to log in with provided credentials.")

    token = await get_or_create_token(conn, user["id"])
    user_data = {
        "username": user["username"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "is_staff": user["is_staff"],
    }
    return LoginResponse(token=token, user=json.dumps(user_data))
