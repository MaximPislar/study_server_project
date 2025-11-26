from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database.models import RefreshToken
from sqlalchemy import select


def is_jti_allowed(token: RefreshToken | None) -> bool:

    # stmt = select(RefreshToken).where(
    #     RefreshToken.jti == jti
    # )
    # result = await session.execute(stmt)
    #
    # refresh_token_in_db: RefreshToken | None = result.scalar_one_or_none()

    if not token:
        return False
    if token.revoked:
        return False
    if token.expires_at < datetime.now(timezone.utc):
        return False
    return True
