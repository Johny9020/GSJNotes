from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import models
import bcrypt
from database import get_database
from fastapi import Security, Depends, status, HTTPException

api_key_header = APIKeyHeader(name='GSJ_API_KEY')


async def validate_api_key(api_key: str = Security(api_key_header), db: Session = Depends(get_database)):
    db_key = db.query(models.APIKey).filter(models.APIKey.api_key == api_key).first()

    if not db_key:
        raise HTTPException(status_code=403, detail='Invalid API Key')

    return db_key


def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
