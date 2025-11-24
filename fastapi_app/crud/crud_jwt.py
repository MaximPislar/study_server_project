import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database.models import RefreshToken


async def store_refresh_token(
        session: AsyncSession,
        user_id: str,
        expires_at: datetime.datetime,
        device_info: str | None = None
) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        expires_at=expires_at,
        device_info=device_info
    )
    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)
    return refresh_token


async def revoke_refresh_token(
        session: AsyncSession,
        jti: str
) -> None:
    # TODO обработка ошибок при работе с бд. Глобальный обработчик?
    stmt = select(RefreshToken).where(
        RefreshToken.jti == jti
    )
    result = await session.execute(stmt)

    refresh_token: RefreshToken | None = result.scalar_one_or_none()

    if refresh_token:
        refresh_token.revoked = True
        await session.commit()
    else:
        raise HTTPException(    # TODO сделать с этим что-то
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JWT not found"
        )

