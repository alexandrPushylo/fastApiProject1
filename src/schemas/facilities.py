from pydantic import BaseModel


class FacilitiesDto(BaseModel):
    title: str


class FacilitiesAdd(FacilitiesDto):
    pass


class Facilities(FacilitiesDto):
    id: int


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facilities_id: int


class RoomFacilities(RoomFacilitiesAdd):
    id: int



