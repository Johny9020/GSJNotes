from pydantic import BaseModel, Field


class ApiKeyScheme(BaseModel):
    api_key: str
