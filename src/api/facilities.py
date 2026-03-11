from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesDto, FacilitiesAdd
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Создать удобство")
async def create_facility(db: DBDep, data: FacilitiesDto = Body()):
    facility = await FacilityService(db).create_facility(data)
    return {"status": "OK", "data": facility}
