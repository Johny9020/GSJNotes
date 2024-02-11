from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    Error: dict


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_dict = {}
    for error in exc.errors():
        field_name = error['loc'][-1]
        error_msg = error['msg']
        error_dict[field_name] = error_msg
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'Error': error_dict})
