class AppError(Exception):
    """Базовое исключение приложения"""

    def __init__(self, message: str, *, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class NotFoundError(AppError):
    """Объект не найден"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class ValidationError(AppError):
    """Ошибка бизнес-логики"""

    def __init__(self, message: str = "Invalid data"):
        super().__init__(message, status_code=400)
