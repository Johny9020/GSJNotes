from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class NotificationModel(Base):
    __tablename__ = 'notifications'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()).replace('-', '_'))
    due_date = Column(DateTime, default=datetime.now())
    diary_entry_id = Column(String, ForeignKey('diary_entries.id'))

    diary_entry = relationship("DiaryEntry", back_populates='notifications')
