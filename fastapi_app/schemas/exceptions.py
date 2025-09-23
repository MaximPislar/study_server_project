from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str
