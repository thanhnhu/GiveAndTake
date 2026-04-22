from fastapi import APIRouter, HTTPException, Request, Response

from core.security import can_edit
from core.utils import to_bool, to_int
from dependencies import CurrentUser, DBConn, OptionalUser
from repositories.giver import GiverRepository
from schemas.giver import GiverCreate, GiverOut, GiverUpdate, PaginatedGivers

router = APIRouter(tags=["Givers"])


@router.get("/api/givers/", response_model=PaginatedGivers)
async def list_givers(request: Request, conn: DBConn, user: OptionalUser) -> PaginatedGivers:
    q = request.query_params
    return await GiverRepository(conn).list(
        user=user,
        page=to_int(q.get("page"), 1),
        page_size=min(to_int(q.get("page_size"), 30), 1000),
        city=q.get("city"),
        number=q.get("number"),
        name=q.get("name"),
        phone=q.get("phone"),
        is_mine=to_bool(q.get("isMine"), False),
    )


@router.post("/api/givers/", response_model=GiverOut, status_code=201)
async def create_giver(payload: GiverCreate, conn: DBConn, user: CurrentUser) -> GiverOut:
    return await GiverRepository(conn).create(user["id"], payload)


@router.patch("/api/givers/{giver_id}/", response_model=GiverOut)
async def update_giver(giver_id: str, payload: GiverUpdate, conn: DBConn, user: CurrentUser) -> GiverOut:
    repo = GiverRepository(conn)
    owner_id = await repo.get_owner(giver_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Not found")
    if not can_edit(owner_id, user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return await repo.update(giver_id, payload, user)


@router.delete("/api/givers/{giver_id}")
@router.delete("/api/givers/{giver_id}/")
async def delete_giver(giver_id: str, conn: DBConn, user: CurrentUser) -> dict:
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    result = await GiverRepository(conn).delete(giver_id, user)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.patch("/api/givers/{giver_id}/set_active/")
async def toggle_giver_active(giver_id: str, conn: DBConn, user: CurrentUser) -> Response:
    repo = GiverRepository(conn)
    owner_id = await repo.get_owner(giver_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Not found")
    if not can_edit(owner_id, user):
        raise HTTPException(status_code=403, detail="Permission denied")
    await repo.toggle_active(giver_id)
    return Response(status_code=200)
