import uuid
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_app.auth import is_jti_allowed
from fastapi_app.auth.dependencies import get_current_active_user_from_token
from fastapi_app.auth.jwt_utils import verify_token, token_type_check
from fastapi_app.core import settings, ACCESS_TOKEN, REFRESH_TOKEN
from fastapi_app.crud import revoke_refresh_token, store_refresh_token
from fastapi_app.database import db_helper, User
from fastapi_app.schemas import UserResponse, ErrorResponseModel, RefreshRequest
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
    jti = str(uuid.uuid4())
    refresh_token_expire = datetime.now() + settings.auth.refresh_token_expire_days
    # TODO проверка на активность

    await store_refresh_token(
        session=session,
        jti=jti,
        user_id=user_id,
        expires_at=refresh_token_expire
    )

    # тут мы создаём jwt токен
    access_token = create_jwt(
        data={"sub": user_id},
        token_type=ACCESS_TOKEN
    )
    refresh_token = create_jwt(
        data={"sub": user_id},
        expire=refresh_token_expire,
        token_type=REFRESH_TOKEN,
        jti=jti
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
    # TODO выдавать токены в куки


@router.post("/refresh", response_model=Token)
async def refresh(
        request: RefreshRequest,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    token_type_check(request.token, REFRESH_TOKEN)
    payload: dict = verify_token(request.token)
    # TODO проверка на активность

    jti = payload.get("jti")
    if not jti:
        raise HTTPException(    # TODO инвалид токен?
            status_code=status.HTTP_404_NOT_FOUND,
            detail="jti not found"
        )
    # TODO сессии ?
    # проверить jti. если jti уже revoked -> возможно replay attack — отозвать все сессии

    allowed = await is_jti_allowed(session, jti)
    if not allowed:
        # либо просто отказать:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or unknown"
        )
    # отозвать старый рефреш
    await revoke_refresh_token(
        session=session,
        jti=jti
    )
    new_jti = str(uuid.uuid4())
    data = {"sub": payload.get("sub")}
    # TODO добавить expire в create_jwt?
    expire = datetime.now() + settings.auth.refresh_token_expire_days

    # сохранить новый рефреш в бд
    # TODO при выдаче нового токена, ревокать ВСЕ токены из базы. Или пора внедрять сессию
    await store_refresh_token(
        session=session,
        jti=new_jti,
        user_id=data["sub"],
        expires_at=expire     # TODO не бесконечная рефреш сессия
    )

    access_token = create_jwt(
        data=data,
        token_type=ACCESS_TOKEN
    )

    refresh_token = create_jwt(
        data=data,
        expire=expire,
        token_type=REFRESH_TOKEN,
        jti=new_jti
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
    # TODO выдавать токены в куки


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
