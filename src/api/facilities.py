import json

from fastapi import Query, APIRouter, Body, HTTPException


from src.api.dependencies import DBDep, UserIdDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesDto, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schema: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities", facilities_json)
        return facilities

    else:
        facilities_dict = json.loads(facilities_from_cache)
        return facilities_dict
    # return await db.facilities.get_all()


@router.post("", summary="Создать удобство")
async def create_facility(
        db: DBDep,
        user_id: UserIdDep,
        data: FacilitiesDto = Body()
):
    facility = FacilitiesAdd(**data.model_dump())
    result = await db.facilities.add(facility)
    await db.commit()
    return {"status": "OK", "data": result}


