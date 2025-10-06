from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database import db_helper
from fastapi_app.schemas.token import Token

router = APIRouter(
    prefix="/security",
    tags=["Security"]
)


@router.post("/token", response_model=Token)
async def login(
        creds: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    pass
