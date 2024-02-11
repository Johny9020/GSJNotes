from typing import List
from fastapi import FastAPI
from fastapi.middleware import Middleware
from config import settings
from fastapi.exceptions import RequestValidationError
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from endpoints.users import router as user_router
from endpoints.admin import router as admin_router
from error_handlers.RequestValidationHandler import validation_exception_handler
from error_handlers.UserError import UserException, user_exception_handler


def initialize_routers(app_: FastAPI) -> None:
    app_.include_router(user_router)
    app_.include_router(admin_router)


def initialize_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(exc_class_or_status_code=RequestValidationError, handler=validation_exception_handler)
    app_.add_exception_handler(exc_class_or_status_code=UserException, handler=user_exception_handler)


def initialize_middleware() -> List[Middleware]:
    origins = [
        'http://localhost:8000'
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
        middleware=initialize_middleware()
    )
    initialize_handlers(app_=app_)
    initialize_routers(app_=app_)
    return app_


app = create_app()

models.Base.metadata.create_all(bind=engine)
