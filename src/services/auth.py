from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def veryfy_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ASSISTANT_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)


    def decode_token(self, token) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
