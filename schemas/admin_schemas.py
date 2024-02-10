from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str = Field(min_length=1)
