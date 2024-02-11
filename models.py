import uuid
from sqlalchemy import Boolean, Column, String, Integer, DateTime, func
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True, index=True, default=str(uuid.uuid4()).replace('-', '_'))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class APIKey(Base):
    __tablename__ = 'api_keys'

    id = Column(String, primary_key=True, unique=True, index=True, default=str(uuid.uuid4()).replace('-', '_'))
    api_key = Column(String, index=True, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
