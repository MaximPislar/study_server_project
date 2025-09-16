from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str, error_code: str, status_code: int = 404):
        self.error_code = error_code
        super().__init__(detail=detail, status_code=status_code)


class InvalidUserDataException(HTTPException):
    def __init__(self, detail: str, error_code: str, status_code: int = 409):
        self.error_code = error_code
        super().__init__(detail=detail, status_code=status_code)
