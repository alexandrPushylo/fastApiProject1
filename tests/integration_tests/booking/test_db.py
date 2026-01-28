import datetime

from schemas.bookings import BookingAdd


async def test_add_crud(db):
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
    booking = await db.bookings.get_one_or_none(room_id=room.id, user_id=user.id)
    assert booking.price == booking_data.price
    assert booking.room_id == booking_data.room_id

    new_booking_data = BookingAdd(
        room_id=room.id,
        date_from=datetime.date(2021, 1, 2),
        date_to=datetime.date(2021, 1, 5),
        user_id=user.id,
        price=1000,
    )
    await db.bookings.edit(new_booking_data, id=booking.id)
    edited_booking = await db.bookings.get_one_or_none(id=booking.id)

    assert edited_booking.price == new_booking_data.price
    assert edited_booking.date_from == new_booking_data.date_from
    assert edited_booking.date_to == new_booking_data.date_to

    await db.bookings.delete(id=edited_booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=edited_booking.id)
    assert not deleted_booking

    await db.commit()
