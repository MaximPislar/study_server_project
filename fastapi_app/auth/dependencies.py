from typing import Annotated, Type

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.auth.utils import decode_acces_token
from fastapi_app.database import db_helper, User
from fastapi_app.exceptions_and_handlers import InvalidTokenException, InvalidUserDataException
from fastapi_app.schemas import PayloadModel
from fastapi_app.core import ACCESS_TOKEN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")


async def get_current_active_user_from_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> Type[User]:

    try:
        payload: PayloadModel = decode_acces_token(token)

    except jwt.exceptions.DecodeError:
        raise InvalidTokenException(
            detail="Invalid token"
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidTokenException(
            detail="Token has expired"
        )
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenException(
            detail="Invalid token"
        )

    user = await session.get(User, payload.sub)

    if user is None:
        raise InvalidUserDataException(
            detail="Invalid token"
        )

    return user
