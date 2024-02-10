import os
from fastapi import APIRouter, Response, status, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
import models
from database import get_database

router = APIRouter(prefix='/api/admin')


def check_admin(user_info: dict, db: Session = Depends()):
    username = user_info.get('username')
    password = user_info.get('password')

    if username != os.getenv('ADMIN_USERNAME') or password != os.getenv('ADMIN_PASSWORD'):
        return False

    return True


@router.get('/')
async def get_admin(response: Response, user_info: dict, db: Session = Depends(get_database)):
    if not check_admin(user_info, db):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'status': response.status_code, 'error': 'Failed to authorize admin!'}

    access_tokens = db.query(models.AccessToken).all()
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

    admin_model = models.AccessToken()
    admin_model.access_token = str(uuid4())

    db.add(admin_model)
    db.commit()
    db.refresh(admin_model)
    response.status_code = status.HTTP_201_CREATED

    return {'status': response.status_code, 'access_token': admin_model.access_token}


