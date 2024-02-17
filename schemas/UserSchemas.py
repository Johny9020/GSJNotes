from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    is_active: bool = Field()


class UserDelete(BaseModel):
    user_id: str = Field(min_length=1)


class UserID(BaseModel):
    id: str = Field(min_length=1)
