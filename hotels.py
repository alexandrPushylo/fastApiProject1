from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {
        "id": 1,
        "title": "Hotel 1",
        "name": "Hotel 1",
    },
    {
        "id": 2,
        "title": "Hotel 2",
        "name": "Hotel 2",
    },
]


@router.get("", summary="Получить список отелей")
def get_hotels(
        hotel_id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description="Hotel Name"),
        title: str | None = Query(None, description="Hotel Title"),
):
    hotels_filtered = []
    for hotel in hotels:
        if hotel_id and hotel['id'] != hotel_id:
            continue
        if name and hotel['name'] != name:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_filtered.append(hotel)
    return hotels_filtered


@router.post("", summary="Создать отель")
def create_hotel(
        data: Hotel = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "name": "sochi_u_morya",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "name": "dubai_fountain",
                }
            }
        })
):
    hotels.append({
        "id": len(hotels) + 1,
        "name": data.name,
        "title": data.title,
    })
    return {"success": True}


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {"success": True}


@router.put("/{hotel_id}", summary="Обновить отель")
def update_hotel(
        hotel_id: int,
        data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = data.name
            hotel['title'] = data.title

    return {"success": True}


@router.patch("/{hotel_id}", summary="Частично обновить отель")
def patch_hotel(
        hotel_id: int,
        data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if data.name:
                hotel['name'] = data.name
            if data.title:
                hotel['title'] = data.title

    return {"success": True}
