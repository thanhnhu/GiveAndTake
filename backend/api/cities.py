from fastapi import APIRouter

from dependencies import DBConn
from repositories.city import CityRepository
from schemas.city import CityOut

router = APIRouter(tags=["Cities"])


@router.get("/api/cities/", response_model=list[CityOut])
async def list_cities(conn: DBConn) -> list[CityOut]:
    return await CityRepository(conn).list_all()
