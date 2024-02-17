from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserException(Exception):
    def __init__(self, status_code: int, details: str):
        self.status_code = status_code
        self.details = details


async def user_exception_handler(request: Request, exc: UserException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': exc.status_code, 'Error': exc.details}
    )
