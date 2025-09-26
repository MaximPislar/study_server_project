from typing import Annotated

from fastapi import APIRouter, Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database import db_helper
from fastapi_app.schemas.exceptions import ErrorResponseModel
from fastapi_app.schemas.user import UserResponse, UserRegistration
from fastapi_app.crud import create_user, get_user_by_username

router = APIRouter(
    tags=['User'],
    prefix='/user'
)


@router.get(
    path='/{username}',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Return user information by username",
    responses={
        status.HTTP_200_OK: {"model": UserResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseModel}
}
)
async def get_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        username: Annotated[str, Path(title="Username")]
):
    user = await get_user_by_username(session, username)
    return user


@router.post(
    path="/registration",
    description="Registration of new user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": UserResponse},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseModel}
    }

)
async def registration(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_creds: UserRegistration
):
    new_user = await create_user(session, user_creds)
    return new_user
