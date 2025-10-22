from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserAdd


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserAdd):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.schema.model_validate(model, from_attributes=True)
        except IntegrityError:
            raise ValueError('User already exists')



