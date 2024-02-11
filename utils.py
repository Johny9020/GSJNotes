from sqlalchemy.orm import Session
import models
import bcrypt


def check_access_token(db: Session, access_token: str):
    access_token = db.query(models.AccessToken).filter(models.AccessToken.access_token == access_token).first()

    if not access_token:
        return False
    return True


def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
