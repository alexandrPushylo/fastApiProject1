import datetime

from schemas.bookings import BookingAdd


async def test_add_booking(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAdd(
        room_id=room.id,
        date_from=datetime.date(2021, 1, 1),
        date_to=datetime.date(2021, 1, 2),
        user_id=user.id,
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.commit()
