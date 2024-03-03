from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class NotificationCreate(BaseModel):
    due_date: datetime


class DiaryEntryCreate(BaseModel):
    title: str
    content: str = None
