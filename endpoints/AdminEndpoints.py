import os
from fastapi import APIRouter, Response, status, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
import models
from database import get_database
from config import settings

router = APIRouter(prefix='/api/admin', tags=['Admin endpoints'])


def check_admin(user_info: dict, db: Session = Depends()):
    username = user_info.get('username')
    password = user_info.get('password')

    if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
        return False

    return True


@router.get('/')
async def get_admin(response: Response, user_info: dict, db: Session = Depends(get_database)):
    if not check_admin(user_info, db):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'status': response.status_code, 'error': 'Failed to authorize admin!'}

    access_tokens = db.query(models.APIKey).all()
    response.status_code = status.HTTP_200_OK

    return {
        'status': response.status_code,
        'access_tokens': access_tokens
    }


@router.post('/cas')
async def create_access_token(response: Response, user_info: dict, db: Session = Depends(get_database)):
    if not check_admin(user_info, db):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'status': response.status_code, 'error': 'Failed to authorize admin!'}

    admin_model = models.APIKey()
    admin_model.api_key = f'gsj_apk_{str(uuid4()).replace('-', '')}'

    db.add(admin_model)
    db.commit()
    db.refresh(admin_model)
    response.status_code = status.HTTP_201_CREATED

    return {'status': response.status_code, 'access_token': admin_model.api_key}


