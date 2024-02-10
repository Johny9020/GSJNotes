from sqlalchemy.orm import Session
import models
from fastapi import Response, status, Depends
from schemas.admin_schemas import AccessToken


def check_access_token(db: Session, access_token: str):
    access_token = db.query(models.AccessToken).filter(models.AccessToken.access_token == access_token).first()

    if not access_token:
        return False
    return True

