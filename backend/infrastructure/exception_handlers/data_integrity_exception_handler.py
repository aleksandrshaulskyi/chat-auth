from fastapi import Request
from fastapi.responses import JSONResponse

from application.exceptions import DataIntegrityException


async def data_integrity_exception_handler(request: Request, exception: DataIntegrityException):
    content = {'title': exception.title, **exception.details}

    return JSONResponse(
        status_code=400,
        media_type='application/problem+json',
        content=content,
    )
