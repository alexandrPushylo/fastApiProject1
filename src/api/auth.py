from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, IncorrectPasswordException, IncorrectPasswordHTTPException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login", summary="Авторизация пользователя")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "ok"}


@router.get("/me", summary="Проверка токена")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_one_or_none_user(user_id=user_id)


@router.post("/logout", summary="Выход пользователя")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
