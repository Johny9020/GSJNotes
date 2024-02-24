from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(min_length=1)
    content: str


class NoteID(BaseModel):
    id: str


class NoteUpdate(BaseModel):
    title: str = Field(min_length=1)
    content: str
