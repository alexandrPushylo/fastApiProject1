from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper, UserWithHashedPasswordDataMapper
from src.schemas.users import UserAdd, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def add(self, data: UserAdd):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise ValueError('User already exists')

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
