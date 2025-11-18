from datetime import date

from pydantic import BaseModel


class BookingAddDto(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddDto):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int



