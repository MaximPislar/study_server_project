from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from fastapi_app.auth.jwt_utils import verify_token, token_type_check
from fastapi_app.database import db_helper, User
from fastapi_app.exceptions_and_handlers import InvalidUserDataException
from fastapi_app.core import ACCESS_TOKEN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_active_user_from_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> Type[User]:
    token_type_check(token, ACCESS_TOKEN)
    payload: dict = verify_token(token)

    try:
        user = await session.get(User, payload.get("sub"))
    except SQLAlchemyError as e:
        print(e)    # TODO нормальная обработка ошибок при работе с бд
        user = None

    if user is None:
        raise InvalidUserDataException(
            detail="Invalid token"
        )

    return user
