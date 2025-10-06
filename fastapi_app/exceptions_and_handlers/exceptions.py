from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str, error_code: str, status_code: status.HTTP_404_NOT_FOUND):
        self.error_code = error_code
        super().__init__(detail=detail, status_code=status_code)


class InvalidUserDataException(HTTPException):
    def __init__(self, detail: str, error_code: str, status_code: status.HTTP_409_CONFLICT):
        self.error_code = error_code
        super().__init__(detail=detail, status_code=status_code)


class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str, error_code: str, status_code: status.HTTP_401_UNAUTHORIZED):
        self.error_code = error_code
        super().__init__(detail=detail, status_code=status_code)
