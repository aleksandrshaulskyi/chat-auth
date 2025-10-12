







from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def pydantic_validation_exception_handler(request: Request, exception: ValidationError):
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