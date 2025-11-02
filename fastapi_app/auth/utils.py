from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi_app.core import settings, ACCESS_TOKEN, REFRESH_TOKEN
from fastapi_app.database import User
from fastapi_app.exceptions_and_handlers import UserIsInactiveException
from fastapi_app.schemas import PayloadModel


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def verify_user(
        session: AsyncSession,
        username: str
) -> User:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


def verify_password(
        db_password: str,
        user_password: str
) -> bool:
    if bcrypt.checkpw(user_password.encode(), db_password.encode()):
        return True
    return False


async def authenticate_user(
        session: AsyncSession,
        username: str,
        password: str
) -> User | bool:
    user = await verify_user(
        session=session,
        username=username
    )

    if not user:
        return False

    is_password_ok = verify_password(
        db_password=user.password,
        user_password=password
    )

    if not is_password_ok:
        return False

    if not user.is_active:
        raise UserIsInactiveException(
            detail="User is inactive"
        )

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({
        "exp": expire,
        "type": ACCESS_TOKEN
    })
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.auth.private_key_path.read_text(),
        algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({
        "exp": expire,
        "type": REFRESH_TOKEN
    })
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.auth.private_key_path.read_text(),
        algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> PayloadModel:
    payload = jwt.decode(
        jwt=token,
        key=settings.auth.public_key_path.read_text(),
        algorithms=[settings.auth.algorithm]
    )
    return PayloadModel(**payload)
