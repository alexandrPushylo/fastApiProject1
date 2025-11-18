from fastapi import Query, APIRouter, Body, HTTPException


from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddDto, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        data: BookingAddDto = Body()
):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
    result = await db.bookings.add(booking)
    await db.commit()
    return {"status": "OK", "data": result}


