from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all_rooms_by_hotel_id(self, hotel_id: int):
        query = select(self.model).where(self.model.hotel_id == hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(self.model, from_attributes=True) for self.model in result.scalars().all()]



