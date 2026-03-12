from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from schemas.users import UserRequestAdd, UserAdd
from src.config import settings
from src.exceptions import IncorrectTokenException, EmailNotRegisteredException, IncorrectPasswordException, ObjectAlreadyExistsException, UserAlreadyExistsException
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ASSISTANT_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)

    def decode_token(self, token) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Время действия токена завершено")

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as e:
            raise UserAlreadyExistsException from e

    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)