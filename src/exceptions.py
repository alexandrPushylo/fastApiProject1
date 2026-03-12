from datetime import date

from fastapi.exceptions import HTTPException


class RentBaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(RentBaseException):
    detail = "Объект не найден"


class HotelNotFoundException(RentBaseException):
    detail = "Отель не найден"


class RoomNotFoundException(RentBaseException):
    detail = "Номер не найден"


class ObjectAlreadyExistsException(RentBaseException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(RentBaseException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(RentBaseException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(RentBaseException):
    detail = "Пользователь с таким Email не зарегистрирован"


class IncorrectPasswordException(RentBaseException):
    detail = "Пароль неверный"


class UserAlreadyExistsException(RentBaseException):
    detail = "Пользователь уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class RentBaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(RentBaseHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(RentBaseHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(RentBaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(RentBaseHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(RentBaseHTTPException):
    status_code = 401
    detail = "Пользователь с таким Email не зарегистрирован"


class IncorrectPasswordHTTPException(RentBaseHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class UserEmailAlreadyExistsHTTPException(RentBaseHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class NoAccessTokenHTTPException(RentBaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"