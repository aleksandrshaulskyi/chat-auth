from fastapi import Request
from fastapi.responses import JSONResponse

from infrastructure.exceptions import InfrastructureException


async def infrastructure_exception_handler(request: Request, exception: InfrastructureException):
    content = {'title': exception.title, **exception.details}

    return JSONResponse(
        status_code=401,
        media_type='application/problem+json',
        content=content,
    )
