from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

# hotels = [
#     {"id": 1, "title": "Hotel 1", "name": "Hotel 1"},
#     {"id": 2, "title": "Hotel 2", "name": "Hotel 2"},
#     {"id": 3, "title": "Sochi", "name": "sochi"},
#     {"id": 4, "title": "Дубай", "name": "dubai"},
#     {"id": 5, "title": "Мальдивы", "name": "maldivi"},
#     {"id": 6, "title": "Геленджик", "name": "gelendzhik"},
#     {"id": 7, "title": "Москва", "name": "moscow"},
#     {"id": 8, "title": "Казань", "name": "kazan"},
#     {"id": 9, "title": "Санкт-Петербург", "name": "spb"},
# ]


@router.get("", summary="Получить список отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel Location"),
        title: str | None = Query(None, description="Hotel Title")
):
    async with async_session_maker() as session:
        limit = pagination.per_page
        offset = (pagination.page - 1) * pagination.per_page
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=limit,
            offset=offset
        )


@router.post("", summary="Создать отель")
async def create_hotel(
        data: Hotel = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {"success": True}


@router.put("/{hotel_id}", summary="Обновить отель")
async def update_hotel(
        hotel_id: int,
        data: Hotel,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить отель")
def patch_hotel(
        hotel_id: int,
        data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if data.name:
                hotel['name'] = data.name
            if data.title:
                hotel['title'] = data.title

    return {"success": True}
