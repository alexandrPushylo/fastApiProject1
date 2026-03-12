from fastapi import APIRouter, Body

from src.exceptions import AllRoomsAreBookedHTTPException, AllRoomsAreBookedException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddDto
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: BookingAddDto = Body()):
    try:
        booking = await BookingService(db).add_booking(user_id=user_id, booking_data=data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me", summary="Получить все бронирования пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)
