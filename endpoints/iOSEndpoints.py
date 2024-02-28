from fastapi import APIRouter
from config import settings
from fastapi.responses import JSONResponse
from schemas.AuthSchemas import AuthInfo

from error_handlers.UserError import UserException

router = APIRouter(prefix='/api/ios', tags=['iOS Endpoints'])


@router.get('')
async def index(auth_info: AuthInfo):
    if auth_info.username != 'johny' and auth_info.password != '012060':
        raise UserException(status_code=401, details='Invalid authentication')

    ios_host = settings.IOS_HOST
    ios_port = settings.IOS_PORT
    ios_database_port = settings.IOS_DATABASE_PORT

    return JSONResponse(status_code=200, content={'ios_host': ios_host, 'ios_port': ios_port,
                                                  'ios_database_port': ios_database_port})
