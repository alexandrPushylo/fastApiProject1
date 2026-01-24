from database import async_session_maker_null_pool
from schemas.hotels import HotelAdd
from utils.db_manager import DBManager


async def test_add_hotels():
    hotel_data = HotelAdd(title="Azure", location="Sochi")

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()

        print(new_hotel)
        assert new_hotel.title == "Azure"