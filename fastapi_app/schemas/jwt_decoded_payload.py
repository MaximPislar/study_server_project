from pydantic import BaseModel


class PayloadModel(BaseModel):
    sub: str
    exp: int
