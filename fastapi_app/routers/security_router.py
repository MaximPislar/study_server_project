from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core import settings
from fastapi_app.database import db_helper
from fastapi_app.schemas.token import Token
from fastapi_app.exceptions_and_handlers import InvalidCredentialsException
from fastapi_app.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/security",
    tags=["Security"]
)


@router.post("/token", response_model=Token)
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
    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)
