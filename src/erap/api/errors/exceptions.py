class ApplicationError(Exception):
    """Base exception for expected application errors."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)