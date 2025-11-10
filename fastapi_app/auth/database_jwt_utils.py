import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database.models import RefreshToken
from sqlalchemy import select


async def is_jti_allowed(
        session: AsyncSession,
        jti: str
) -> bool:

    stmt = select(RefreshToken).where(
        RefreshToken.jti == jti
    )
    result = await session.execute(stmt)

    refresh_token_in_db: RefreshToken | None = result.scalar_one_or_none()

    if not refresh_token_in_db:
        return False
    if refresh_token_in_db.revoked:
        return False
    if refresh_token_in_db.expires_at < datetime.datetime.utcnow():
        return False
    return True
