from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(
            self,
            detail: str,
            status_code: status.HTTP_404_NOT_FOUND
    ):
        super().__init__(detail=detail, status_code=status_code)


class InvalidUserDataException(HTTPException):
    def __init__(
            self,
            detail: str,
            status_code: status.HTTP_409_CONFLICT
    ):
        super().__init__(detail=detail, status_code=status_code)


class InvalidCredentialsException(HTTPException):
    def __init__(
            self,
            detail: str,
            status_code: status.HTTP_401_UNAUTHORIZED,
            headers: dict = None
    ):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super().__init__(
            detail=detail,
            status_code=status_code,
            headers=headers
        )
