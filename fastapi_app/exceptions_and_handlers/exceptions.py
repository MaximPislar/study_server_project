from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(
            self,
            detail: str = "User not found"
    ):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class InvalidUserDataException(HTTPException):
    def __init__(
            self,
            detail: str = "Invalid user data"
    ):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InvalidCredentialsException(HTTPException):
    def __init__(
            self,
            detail: str = "Invalid username or password",
            headers: dict = None
    ):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers=headers
        )


class UserIsInactiveException(HTTPException):
    def __init__(
            self,
            detail: str = "User is inactive"
    ):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InvalidTokenException(HTTPException):
    def __init__(
            self,
            detail: str = "Invalid token"
    ):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)
