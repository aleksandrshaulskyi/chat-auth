from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=422,
        media_type='application/problem+json',
        content={
            'title': 'Data validation exception',
            'details': {
                item.get('loc')[1]: item.get('msg') for item in exception.errors()
            }
        }
    )