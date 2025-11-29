from pydantic import BaseModel, Field


class RoomAddDto(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPatchDto(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
