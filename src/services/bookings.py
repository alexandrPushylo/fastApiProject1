from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAddDto, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService

class BookingService(BaseService):
    async def add_booking(self, user_id: int, booking_data: BookingAddDto):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e

        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
