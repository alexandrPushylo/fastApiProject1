from fastapi import APIRouter, Body, HTTPException

from src.exceptions import (
    ObjectNotFoundException,
    NotExistsFreeRoomsException,
    RoomNotFoundHTTPException,
)
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddDto, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: BookingAddDto = Body()):
    try:
        room = await db.rooms.get_one(id=data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())

    try:
        result = await db.bookings.add_booking(data=booking, hotel_id=hotel.id)
    except NotExistsFreeRoomsException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": result}


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить все бронирования пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
