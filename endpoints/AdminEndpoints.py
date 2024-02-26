from fastapi import APIRouter, Response, status, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
import models
from database import get_database, engine
from config import settings
from error_handlers.AdminError import AdminException

router = APIRouter(prefix='/api/admin', tags=['Admin endpoints'])


def check_admin(user_info: dict):
    username = user_info.get('username')
    password = user_info.get('password')

    if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
        return False

    return True


# Endpoint https://BASE_URI/api/admin
# Method: GET
# Action: Get all api keys
@router.get('/')
async def get_admin(response: Response, user_info: dict, db: Session = Depends(get_database)):
    if not check_admin(user_info):
        raise AdminException(status_code=401, details="Failed to authorize admin")

    access_tokens = db.query(models.APIKey).all()
    response.status_code = status.HTTP_200_OK

    return {
        'status': response.status_code,
        'api_keys': access_tokens
    }


# Endpoint https://BASE_URI/api/admin/cas
# Method: Post
# Action: Create a new api key
@router.post('/cas')
async def create_access_token(user_info: dict = Depends(check_admin), db: Session = Depends(get_database)):
    if not check_admin(user_info):
        raise AdminException(status_code=401, details="Failed to authorize admin")

    admin_model = models.APIKey()
    admin_model.api_key = 'gsj_apk_' + str(uuid4()).replace('-', '')

    db.add(admin_model)
    db.commit()
    db.refresh(admin_model)

    return {'api_key': admin_model.api_key}


# Endpoint https://BASE_URI/api/admin/delete/{user_id}
# Method: DELETE
# Action: Delete every note that belongs to a specific user id
@router.delete('/delete/{user_id}')
async def delete_user_data(response: Response, user_id: str, user_info: dict, db: Session = Depends(get_database)):
    """ Delete every note that belongs to {user_id} """

    if not check_admin(user_info):
        raise AdminException(status_code=401, details="Failed to authorize admin")

    notes = db.query(models.Note).filter_by(owner_id=user_id)

    if not notes:
        response.status_code = status.HTTP_200_OK
        return {'response': 'User ID: ' + user_id + ', has not note data'}

    notes.delete()
    db.commit()

    return {'response': 'Successfully delete all note data belonging to ' + user_id}


# Endpoint https://BASE_URI/api/admin/reset
# Method: POST
# Action: Reset the entire database
@router.post('/reset')
async def reset_token(user_info: dict, db: Session = Depends(get_database)):
    if not check_admin(user_info):
        raise AdminException(status_code=401, details="Failed to authorize admin")

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db.commit()

    return {'status': 'Successfully deleted database'}
