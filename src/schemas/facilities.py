from pydantic import BaseModel


class FacilitiesDto(BaseModel):
    title: str


class FacilitiesAdd(FacilitiesDto):
    pass


class Facilities(FacilitiesDto):
    id: int



