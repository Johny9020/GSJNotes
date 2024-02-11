from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
import models
from database import get_database
from schemas.user_schemas import User
from schemas.admin_schemas import AccessToken
from utils import check_access_token, encrypt_password

router = APIRouter(prefix='/api/users')


# Endpoint https://BASE_URI/api/users
# Method: GET
# Action: List users
@router.get('/')
async def read_api(response: Response, token_info: AccessToken, db: Session = Depends(get_database)):

    if not check_access_token(db, token_info.access_token):
        return {'error': 'The access token is invalid.'}

    users = db.query(models.User).all()

    if not users:
        return {'message': 'There are currently no users registered!'}

    return {'users': users}


# Endpoint https://BASE_URI/api/users
# Method: Post
# Action: Create user
@router.post('/')
async def create_user(response: Response, user: User, token_info: AccessToken, db: Session = Depends(get_database)):
    if not check_access_token(db, token_info.access_token):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            'status': response.status_code,
            'error': 'Could not validate access token!'
        }

    existing_user = db.query(models.User).filter_by(username=user.username).first()

    if existing_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status_code': response.status_code, 'error': "Username already taken"}

    user_model = models.User()
    user_model.username = user.username
    user_model.hashed_password = encrypt_password(user.hashed_password)
    user_model.is_active = user.is_active

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    response.status_code = status.HTTP_201_CREATED

    return {
        'status': response.status_code,
        'data': user_model
    }


# Endpoint https://BASE_URI/api/users/?id={id}
# Method: DELETE
# Action: Delete user
@router.delete('/')
async def delete_user(response: Response, user: dict, token_info: AccessToken, db: Session = Depends(get_database)):
    if not check_access_token(db, token_info.access_token):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            'status': response.status_code,
            'error': 'Could not authenticate access token'
        }

    user_id = user.get('user_id')
    user = db.query(models.User).filter_by(id=user_id).first()

    if not user:
        response.status_code = status.HTTP_400_BAD_REQUEST

        return {'status': response.status_code, 'user_id': user_id, 'error': "User not found"}

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}