from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddDto, RoomPatchDto


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер отеля")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    result = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Номер с id {room_id} не найден")
    return result


@router.get("/{hotel_id}/rooms", summary="Получить список номеров отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(
        db: DBDep,
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
    room = await db.rooms.add(room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    count_rooms = await db.rooms.count(id=room_id)
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

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_room(
        hotel_id: int,
        room_id: int,
        data: RoomAddDto,
        db: DBDep
):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    count_rooms = await db.rooms.count(id=room_id)
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
    await db.rooms.edit(room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def patch_room(
        hotel_id: int,
        room_id: int,
        data: RoomPatchDto,
        db: DBDep
):
    room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump())
    count_rooms = await db.rooms.count(id=room_id)
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
    await db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
