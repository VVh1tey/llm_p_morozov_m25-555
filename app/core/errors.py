class AppError(Exception):
    pass


# email уже занят
class ConflictError(AppError):
    pass


# неверный пароль или пользователь не найден
class UnauthorizedError(AppError):
    pass


class ForbiddenError(AppError):
    pass


# объект не найден в базе
class NotFoundError(AppError):
    pass


# openrouter вернул ошибку
class ExternalServiceError(AppError):
    pass
