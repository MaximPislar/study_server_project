from datetime import timedelta, datetime, timezone

import jwt

from fastapi_app.core import settings


def create_jwt(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({
        "exp": expire,
        "type": token_type
    })
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.auth.private_key_path.read_text(),
        algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        jwt=token,
        key=settings.auth.public_key_path.read_text(),
        algorithms=[settings.auth.algorithm]
    )
    return payload
