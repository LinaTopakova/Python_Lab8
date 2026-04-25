class CustomExceptionA(Exception):
    """Исключение для сценария A (например, конфликт данных)."""
    def __init__(self, message: str = "Custom A error", status_code: int = 409):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class CustomExceptionB(Exception):
    """Исключение для сценария B (например, ресурс не найден)."""
    def __init__(self, message: str = "Custom B error", status_code: int = 404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
