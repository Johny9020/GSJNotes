from sqlalchemy import Column, String, Boolean
from uuid import uuid4
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True, index=True, default=str(uuid4()).replace('-', '_'))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)