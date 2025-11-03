from datetime import timedelta, datetime, timezone

import jwt

from fastapi_app.core import settings, TOKEN_TYPE_FIELD
from fastapi_app.exceptions_and_handlers import InvalidTokenException


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


def verify_token(token: str) -> dict | None:
    try:
        payload: dict = decode_access_token(token)

    except jwt.exceptions.DecodeError:
        raise InvalidTokenException(
            detail="Invalid token"
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidTokenException(
            detail="Token has expired"
        )
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenException(
            detail="Invalid token"
        )
    if not payload:
        raise InvalidTokenException(
            detail="Invalid token"
        )

    return payload


def token_type_check(payload: dict, checked_type: str) -> None:
    if not payload.get(TOKEN_TYPE_FIELD):
        raise InvalidTokenException

    if payload.get(TOKEN_TYPE_FIELD) != checked_type:
        raise InvalidTokenException(
            detail=f"Invalid token type: {checked_type !r} token required"
        )
