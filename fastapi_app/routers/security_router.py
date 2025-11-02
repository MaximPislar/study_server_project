from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_app.auth.dependencies import get_current_active_user_from_token
from fastapi_app.core import settings, ACCESS_TOKEN, REFRESH_TOKEN
from fastapi_app.database import db_helper, User
from fastapi_app.schemas import UserResponse, ErrorResponseModel
from fastapi_app.schemas.token import Token
from fastapi_app.exceptions_and_handlers import InvalidCredentialsException
from fastapi_app.auth import authenticate_user, create_jwt


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=Token)
async def login(
        creds: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    user = await authenticate_user(
        session=session,
        username=creds.username,
        password=creds.password
    )
    if not user:
        raise InvalidCredentialsException(
            detail="Invalid username or password"
        )

    user_id = str(user.id)

    # тут мы создаём jwt токен
    access_token = create_jwt(
        data={"sub": user_id},
        expires_delta=settings.auth.access_token_expire_minutes,
        token_type=ACCESS_TOKEN
    )
    refresh_token = create_jwt(
        data={"sub": user_id},
        expires_delta=settings.auth.refresh_token_expire_days,
        token_type=REFRESH_TOKEN
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get(
    path='/me',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Returns information about the logged-in user",
    responses={
        status.HTTP_200_OK: {"model": UserResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseModel},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseModel}
    }

    # TODO довести модели ошибок до ума
)
async def get_user(
        current_user: Annotated[User, Depends(get_current_active_user_from_token)]
):
    return current_user
