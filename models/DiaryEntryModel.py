from database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class DiaryEntry(Base):
    __tablename__ = 'diary_entries'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()).replace('-', '_'))
    title = Column(String, default='Entry')
    content = Column(String, nullable=True, default=None)
    created_at = Column(String, default=datetime.now().strftime('%d.%m.%Y'))

    notifications = relationship('NotificationModel', back_populates='diary_entry')
