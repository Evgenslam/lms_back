from fastapi import HTTPException, status


class UserException(
    HTTPException
):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = "Ошибка пользователя"  # <-- задаем значения по умолчанию

    def __init__(self, status_code=None, detail: str = None):
        super().__init__(
            status_code=status_code or self.status_code,
            detail=detail or self.detail,
        )


class EmailAlreadyExistsException(
    UserException
):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с такой почтой уже существует"


class ObjectAlreadyExistsException(UserException):
    def __init__(self, existing_object):
        self.detail = f"{existing_object} уже существует"
        super().__init__(status_code=self.status_code, detail=self.detail)

    status_code = status.HTTP_409_CONFLICT


class IncorrectEmailOrPasswordException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UnauthorizedException(UserException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = "Пользователь не авторизован"


class UserNotFoundException(UserException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = "Пользователь не найден"


class TokenExpiredException(UserException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = "Срок действия токена истек"


class IncorrectTokenFormatException(UserException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = "Неверный формат токена"
