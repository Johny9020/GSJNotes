from typing import List
from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware import Middleware
from config import settings
from fastapi.exceptions import RequestValidationError
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from endpoints.UserEndpoints import router as user_router
from endpoints.AdminEndpoints import router as admin_router
from endpoints.NoteEndpoints import router as note_router
from endpoints.iOSEndpoints import router as ios_router
from endpoints.EntryEndpoints import router as entry_router
from error_handlers.RequestValidationHandler import validation_exception_handler
from error_handlers.UserError import UserException, user_exception_handler
from error_handlers.DataError import DataException, data_exception_handler
from error_handlers.AdminError import AdminException, admin_exception_handler


def initialize_routers(app_: FastAPI) -> None:
    app_.include_router(user_router)
    app_.include_router(admin_router)
    app_.include_router(note_router)
    app_.include_router(ios_router)
    app_.include_router(entry_router)


def initialize_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(exc_class_or_status_code=RequestValidationError, handler=validation_exception_handler)
    app_.add_exception_handler(exc_class_or_status_code=UserException, handler=user_exception_handler)
    app_.add_exception_handler(exc_class_or_status_code=DataException, handler=data_exception_handler)
    app_.add_exception_handler(exc_class_or_status_code=AdminException, handler=admin_exception_handler)


def initialize_middleware() -> List[Middleware]:
    origins = [
        # 'http://localhost:8000',
        '*'
    ]
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=None if settings.ENVIRONMENT == 'production' else '/docs',
        redoc_url=None if settings.ENVIRONMENT == 'production' else '/redoc',
        middleware=initialize_middleware(),
    )
    initialize_handlers(app_=app_)
    initialize_routers(app_=app_)
    return app_


app = create_app()

models.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    run(app, host=settings.HOST_ADDRESS, port=settings.HOST_PORT)
