from fastapi import APIRouter, HTTPException, Response

from dependencies import CurrentUser, DBConn
from repositories.message import MessageRepository
from schemas.message import MessageCreate, MessageOut

router = APIRouter(tags=["Messages"])


@router.get("/api/messages/", response_model=list[MessageOut])
async def list_messages(conn: DBConn) -> list[MessageOut]:
    return await MessageRepository(conn).list_all()


@router.post("/api/messages/", response_model=MessageOut, status_code=201)
async def create_message(payload: MessageCreate, conn: DBConn, user: CurrentUser) -> MessageOut:
    return await MessageRepository(conn).create(payload)


@router.delete("/api/messages/{message_id}")
@router.delete("/api/messages/{message_id}/")
async def delete_message(message_id: int, conn: DBConn, user: CurrentUser) -> Response:
    deleted = await MessageRepository(conn).delete(message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return Response(status_code=204)
