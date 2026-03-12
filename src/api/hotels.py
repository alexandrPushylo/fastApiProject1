from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundHTTPException
)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        result = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
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
    return await HotelService(db).get_filtered_by_time(
        pagination=pagination, date_from=date_from, date_to=date_to, location=location, title=title
    )


@router.post("", summary="Создать отель")
async def create_hotel(
    db: DBDep,
    data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "sochi_u_morya",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "dubai_fountain",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(data)
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить отель")
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    data: HotelAdd,
):
    await HotelService(db).edit_hotel(hotel_id, data)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить отель")
async def patch_hotel(db: DBDep, hotel_id: int, data: HotelPatch):
    await HotelService(db).edit_hotel_partially(hotel_id, data, exclude_unset=True)
    return {"status": "OK"}
