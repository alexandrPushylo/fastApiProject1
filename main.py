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
        id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description="Hotel Name"),
        title: str | None = Query(None, description="Hotel Title"),
):
    hotels_filtered = []
    for hotel in hotels:
        if id and hotel['id'] != id:
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




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
