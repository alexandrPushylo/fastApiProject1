import os
from datetime import timedelta, datetime, timezone

from fastapi import Query, APIRouter, Body, HTTPException, Response

from passlib.context import CryptContext
import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "bd3f75186a761a5ddf473314dd15b099d25d9455592842813c26e48d33199ca4"
ALGORITHM = "HS256"
ASSISTANT_TOKEN_EXPIRE_MINUTES = 30


def veryfy_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ASSISTANT_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        if not veryfy_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {'access_token': access_token}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except ValueError:
            raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

    return {'status': 'ok'}
