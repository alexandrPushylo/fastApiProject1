from pydantic import BaseModel
from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacilities, RoomFacilitiesAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilities

    async def set_facilities(self, room_id: int, facilities_ids: list[int]):
        f_ids = facilities_ids

        current_facilities_ids_query = select(self.model.facility_id).filter_by(room_id=room_id)
        current_facilities_ids_result = await self.session.execute(current_facilities_ids_query)
        current_facilities_ids: list[int] = current_facilities_ids_result.scalars().all()

        ids_for_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_for_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_for_delete:
            del_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_for_delete)
                )
            )
            await self.session.execute(del_m2m_facilities_stmt)

        if ids_for_insert:
            insert_facilities_stmt = (
                insert(self.model)
                .values(
                    [{"room_id": room_id, "facility_id": f_id} for f_id in ids_for_insert]
                )
            )
            await self.session.execute(insert_facilities_stmt)

