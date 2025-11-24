from datetime import datetime

from pydantic import BaseModel


class RefreshJWTPayload(BaseModel):
    sub: str
    exp: datetime
    type: str
    jti: str
