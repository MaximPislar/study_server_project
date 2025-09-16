from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status, Depends, Body

from fastapi_app.exceptions_and_handlers import UserNotFoundException, InvalidUserDataException
from fastapi_app.schemas import UserRegistration
from fastapi_app.database import User
from fastapi_app.database import db_helper


async def check_user_uniqueness(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_creds: Annotated[UserRegistration, Body()]
):

    stmt = select(User).where(
        or_(User.username == user_creds.username,
            User.email == user_creds.email)
    )
    result = await session.execute(stmt)
    result = result.scalars().first()

    if result:
        raise InvalidUserDataException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username or email are already in use",
            error_code="pridumat'_new_username"
        )
    return True


async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_creds: Annotated[UserRegistration, Body()],
        is_user_unique: Annotated[bool, Depends(check_user_uniqueness)]
) -> User:

    new_user = User(
        username=user_creds.username,
        age=user_creds.age,
        password=user_creds.password,
        email=user_creds.email
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_username(
        session: AsyncSession,
        username: str
) -> User:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        raise UserNotFoundException(
            detail="Пользователя с таким именем не существует",
            error_code="user_not_found_lol_kek",
            status_code=404)

    return user



