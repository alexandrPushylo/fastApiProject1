from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(
        db: DBDep,
        hotel_id: int
):
    result = await db.hotels.get_one_or_none(id=hotel_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Отель с id {hotel_id} не найден"
        )
    return result


@router.get("", summary="Получить список отелей")
@cache(expire=10)
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel Location"),
        title: str | None = Query(None, description="Hotel Title"),
        date_from: date = Query(examples=["2025-01-01"]),
        date_to: date = Query(examples=["2025-02-01"]),
):

    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=limit,
        offset=offset
    )


@router.post("", summary="Создать отель")
async def create_hotel(
        db: DBDep,
        data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "sochi_u_morya",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "dubai_fountain",
                }
            }
        })
):
    hotel = await db.hotels.add(data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(
        db: DBDep,
        hotel_id: int,
):
    count_hotels = await db.hotels.count(id=hotel_id)
    if count_hotels < 1:
        raise HTTPException(
            status_code=404,
            detail=f"Отель не найден"
        )
    if count_hotels > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Найдено несколько отелей"
        )

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить отель")
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelAdd,
):
    count_hotels = await db.hotels.count(id=hotel_id)
    if count_hotels < 1:
        raise HTTPException(
            status_code=404,
            detail=f"Отель не найден"
        )
    if count_hotels > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Найдено несколько отелей"
        )

    await db.hotels.edit(data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить отель")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelPatch
):
    count_hotels = await db.hotels.count(id=hotel_id)
    if count_hotels < 1:
        raise HTTPException(
            status_code=404,
            detail=f"Отель не найден"
        )
    if count_hotels > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Найдено несколько отелей"
        )
    await db.hotels.edit(data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
