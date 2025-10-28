from fastapi import APIRouter, HTTPException, Response


from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        if not AuthService().veryfy_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {'access_token': access_token}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except ValueError:
            raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

    return {'status': 'ok'}
