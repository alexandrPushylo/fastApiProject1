from pydantic import BaseModel


class FacilitiesDto(BaseModel):
    title: str


class FacilitiesAdd(FacilitiesDto):
    pass


class Facility(FacilitiesDto):
    id: int


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilities(RoomFacilitiesAdd):
    id: int



