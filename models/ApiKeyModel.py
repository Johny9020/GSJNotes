from sqlalchemy import Column, String, DateTime, func
from datetime import datetime
from uuid import uuid4
from database import Base


class APIKey(Base):
    __tablename__ = 'api_keys'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()).replace('-', '_'))
    api_key = Column(String, index=True, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
