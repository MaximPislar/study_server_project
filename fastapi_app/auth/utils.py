import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi_app.database import User
from fastapi_app.exceptions_and_handlers import UserIsInactiveException


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
