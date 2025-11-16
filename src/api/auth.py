from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response
):

    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    if not AuthService().veryfy_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {'access_token': access_token}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
        db: DBDep,
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ValueError:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

    return {'status': 'ok'}


@router.get("/me", summary="Проверка токена")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout", summary="Выход пользователя")
async def logout(
        response: Response
):
    response.delete_cookie("access_token")
    return {'status': 'ok'}
