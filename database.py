import os
import sqlite3
import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# register an adapter that converts UUID objects to bytes
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
