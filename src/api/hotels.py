from fastapi import Query, APIRouter, Body, HTTPException


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


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
async def delete_hotel(
        hotel_id: int,
):
    async with async_session_maker() as session:
        count_hotels = await HotelsRepository(session).count(id=hotel_id)
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

        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновить отель")
async def update_hotel(
        hotel_id: int,
        data: Hotel,
):
    async with async_session_maker() as session:
        count_hotels = await HotelsRepository(session).count(id=hotel_id)
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

        await HotelsRepository(session).edit(data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частично обновить отель")
async def patch_hotel(
        hotel_id: int,
        data: HotelPATCH
):
    async with async_session_maker() as session:
        count_hotels = await HotelsRepository(session).count(id=hotel_id)
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
        await HotelsRepository(session).edit(data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
