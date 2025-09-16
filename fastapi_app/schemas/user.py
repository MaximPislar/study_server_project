from pydantic import BaseModel, conint, EmailStr, constr


class UserBaseClass(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr


class User(UserBaseClass):
    password: constr(min_length=8, max_length=16)


class UserRegistration(User):
    pass
