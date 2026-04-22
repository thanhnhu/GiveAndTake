from fastapi import APIRouter, HTTPException

from core.security import can_edit
from dependencies import CurrentUser, DBConn
from repositories.donate import DonateRepository
from schemas.donate import DonateCreate, DonateOut, DonateUpdate

router = APIRouter(tags=["Donates"])


@router.post("/api/donates/", response_model=DonateOut, status_code=201)
async def create_donate(payload: DonateCreate, conn: DBConn, user: CurrentUser) -> DonateOut:
    return await DonateRepository(conn).create(user["id"], payload)


@router.patch("/api/donates/{donate_id}/", response_model=DonateOut)
async def update_donate(donate_id: str, payload: DonateUpdate, conn: DBConn, user: CurrentUser) -> DonateOut:
    repo = DonateRepository(conn)
    owner_id = await repo.get_owner(donate_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Not found")
    if not can_edit(owner_id, user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return await repo.update(donate_id, payload)


@router.delete("/api/donates/{donate_id}")
@router.delete("/api/donates/{donate_id}/")
async def delete_donate(donate_id: str, conn: DBConn, user: CurrentUser) -> dict:
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    result = await DonateRepository(conn).delete(donate_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result
