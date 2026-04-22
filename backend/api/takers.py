from fastapi import APIRouter, HTTPException, Request, Response

from core.security import can_edit
from dependencies import CurrentUser, DBConn, OptionalUser
from repositories.taker import TakerRepository
from schemas.taker import PaginatedTakers, TakerCreate, TakerOut, TakerUpdate
from core.utils import to_bool, to_int

router = APIRouter(tags=["Takers"])


@router.get("/api/takers/", response_model=PaginatedTakers)
async def list_takers(request: Request, conn: DBConn, user: OptionalUser) -> PaginatedTakers:
    q = request.query_params
    return await TakerRepository(conn).list(
        user=user,
        page=to_int(q.get("page"), 1),
        page_size=min(to_int(q.get("page_size"), 30), 1000),
        city=q.get("city"),
        number=q.get("number"),
        name=q.get("name"),
        phone=q.get("phone"),
        is_mine=to_bool(q.get("isMine"), False),
    )


@router.post("/api/takers/", response_model=TakerOut, status_code=201)
async def create_taker(payload: TakerCreate, conn: DBConn, user: CurrentUser) -> TakerOut:
    return await TakerRepository(conn).create(user["id"], payload)


@router.patch("/api/takers/{taker_id}/", response_model=TakerOut)
async def update_taker(taker_id: str, payload: TakerUpdate, conn: DBConn, user: CurrentUser) -> TakerOut:
    repo = TakerRepository(conn)
    owner_id = await repo.get_owner(taker_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Not found")
    if not can_edit(owner_id, user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return await repo.update(taker_id, payload, user)


@router.delete("/api/takers/{taker_id}")
@router.delete("/api/takers/{taker_id}/")
async def delete_taker(taker_id: str, conn: DBConn, user: CurrentUser) -> dict:
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    result = await TakerRepository(conn).delete(taker_id, user)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.patch("/api/takers/{taker_id}/stop_donate/")
async def toggle_stop_donate(taker_id: str, conn: DBConn, user: CurrentUser) -> Response:
    repo = TakerRepository(conn)
    owner_id = await repo.get_owner(taker_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Not found")
    if not can_edit(owner_id, user):
        raise HTTPException(status_code=403, detail="Permission denied")
    await repo.toggle_stop_donate(taker_id)
    return Response(status_code=200)
