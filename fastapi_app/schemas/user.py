from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints


class UserBaseClass(BaseModel):
    username: str
    age: Annotated[int, Field(strict=True, gt=18)]
    email: EmailStr


class User(UserBaseClass):
    password: Annotated[
        str,
        StringConstraints(min_length=8, max_length=16)]


class UserRegistration(User):
    pass


class UserResponse(UserBaseClass):
    pass
