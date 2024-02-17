from database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Note(Base):
    __tablename__ = 'notes'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()).replace('-', '_'))
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    owner_id = Column(String, ForeignKey('users.id'))

    owner = relationship('User', back_populates='notes')
