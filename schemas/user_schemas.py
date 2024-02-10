from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    is_active: bool = Field()
