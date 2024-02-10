import sqlite3
import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'

# register an adapter that converts UUID objects to bytes
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
