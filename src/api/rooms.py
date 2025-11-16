from fastapi import APIRouter, Body, HTTPException


from src.database import async_session_maker

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddDto, RoomPatchDto


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер отеля")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Номер с id {room_id} не найден")
        return result


@router.get("/{hotel_id}/rooms", summary="Получить список номеров отеля")
async def get_rooms(hotel_id: int,):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(
        hotel_id: int,
        data: RoomAddDto = Body(openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандартный номер",
                    "description": "Стандартный номер с видом на море",
                    "price": 1000,
                    "quantity": 2,
                }
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс номер",
                    "description": "Люкс номер с видом на море и видом на горы",
                    "price": 10000,
                    "quantity": 1,
                }
            }
        })
):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        count_rooms = await RoomsRepository(session).count(id=room_id)
        if count_rooms < 1:
            raise HTTPException(
                status_code=404,
                detail=f"Номер не найден"
            )
        if count_rooms > 1:
            raise HTTPException(
                status_code=400,
                detail=f"Найдено несколько номеров"
            )

        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_room(hotel_id: int, room_id: int,  data: RoomAddDto):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        count_rooms = await RoomsRepository(session).count(id=room_id)
        if count_rooms < 1:
            raise HTTPException(
                status_code=404,
                detail=f"Номер не найден"
            )
        if count_rooms > 1:
            raise HTTPException(
                status_code=400,
                detail=f"Найдено несколько номеров"
            )
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def patch_room(hotel_id: int, room_id: int, data: RoomPatchDto):
    room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        count_rooms = await RoomsRepository(session).count(id=room_id)
        if count_rooms < 1:
            raise HTTPException(
                status_code=404,
                detail=f"Номер не найден"
            )
        if count_rooms > 1:
            raise HTTPException(
                status_code=400,
                detail=f"Найдено несколько номеров"
            )
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
