from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


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


@app.get("/hotels")
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


@app.post("/hotels")
def create_hotel(
        name: str = Body(),
        title: str = Body(),
):
    hotels.append({
        "id": len(hotels) + 1,
        "name": name,
        "title": title,
    })
    return {"success": True}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {"success": True}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        name: str = Body(),
        title: str = Body(),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = name
            hotel['title'] = title

    return {"success": True}




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
