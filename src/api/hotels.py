from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)
        if location:
            query = (
                query
                .filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
            )
        if title:
            query = (
                query
                .filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
            )

        query = (
            query
            .limit(pagination.per_page)
            .offset((pagination.page - 1) * pagination.per_page)
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
        create_hotel_stmt = insert(HotelsOrm).values(data.model_dump())
        # print(create_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(create_hotel_stmt)
        await session.commit()
    return {"success": True}


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {"success": True}


@router.put("/{hotel_id}", summary="Обновить отель")
def update_hotel(
        hotel_id: int,
        data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = data.name
            hotel['title'] = data.title

    return {"success": True}


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
