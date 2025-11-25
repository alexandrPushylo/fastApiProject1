from fastapi import Query, APIRouter, Body, HTTPException


from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilitiesDto, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


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


