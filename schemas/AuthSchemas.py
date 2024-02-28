from pydantic import BaseModel, Field


class AuthInfo(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
