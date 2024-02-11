from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
import models
from database import get_database
from schemas.user_schemas import User, UserDelete
from utils import encrypt_password, validate_api_key
from error_handlers.UserError import UserException

router = APIRouter(prefix='/api/users', tags=['User endpoints'])


# Endpoint https://BASE_URI/api/users
# Method: GET
# Action: List users
@router.get('/')
async def read_api(response: Response, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    """ List all registered users """

    users = db.query(models.User).all()

    if not users:
        return {'message': 'There are currently no users registered!'}

    return {'users': users}


# Endpoint https://BASE_URI/api/users
# Method: Post
# Action: Create user
@router.post('/')
async def create_user(response: Response, user: User, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    """ Create a new user """

    existing_user = db.query(models.User).filter_by(username=user.username).first()

    if existing_user:
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, details='User already exists!')

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
async def delete_user(response: Response, user_info: UserDelete, api_key: str = Depends(validate_api_key),
                      db: Session = Depends(get_database)):
    """ Delete a user from the database by his id """

    user = db.query(models.User).filter_by(id=user_info.user_id).first()

    if not user:
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, details='User does not exist')

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
