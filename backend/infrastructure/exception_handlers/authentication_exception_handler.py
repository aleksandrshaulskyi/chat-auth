from fastapi import Request
from fastapi.responses import JSONResponse

from application.exceptions import AuthenticationException


async def authentication_exception_handler(request: Request, exception: AuthenticationException):
    content = {'title': exception.title, **exception.details}

    return JSONResponse(
        status_code=401,
        media_type='application/problem+json',
        content=content,
    )
