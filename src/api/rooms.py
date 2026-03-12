from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomAddDto, RoomPatchDto
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер отеля")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        result = await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return result


@router.get("/{hotel_id}/rooms", summary="Получить список номеров отеля")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2025-01-01"]),
    date_to: date = Query(examples=["2025-02-01"]),
):
    return RoomService(db).get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomAddDto = Body(
        openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандартный номер",
                    "description": "Стандартный номер с видом на море",
                    "price": 1000,
                    "quantity": 2,
                    "facilities_ids": [2],
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс номер",
                    "description": "Люкс номер с видом на море и видом на горы",
                    "price": 10000,
                    "quantity": 1,
                    "facilities_ids": [2],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер отеля")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить номер отеля")
async def update_room(hotel_id: int, room_id: int, data: RoomAddDto, db: DBDep):
    await RoomService(db).edit_room(hotel_id=hotel_id, room_id=room_id, room_data=data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить номер отеля")
async def patch_room(hotel_id: int, room_id: int, data: RoomPatchDto, db: DBDep):
    await RoomService(db).edit_room_partially(hotel_id=hotel_id, room_id=room_id, room_data=data)
    return {"status": "OK"}
