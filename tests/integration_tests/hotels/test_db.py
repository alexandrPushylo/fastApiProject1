from schemas.hotels import HotelAdd


async def test_add_hotels(db):
    hotel_data = HotelAdd(title="Azure", location="Sochi")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()

    assert new_hotel.title == "Azure"