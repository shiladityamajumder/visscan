# File: app/exceptions/handlers.py
# Description: Custom exception handlers for FastAPI to format error responses consistently.


from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

def format_error_response(message: str, code: int = 400):
    return {
        "status": "error",
        "message": message,
        "code": code,
        "data": None
    }

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(exc.detail, exc.status_code)
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=format_error_response("Validation error", 422)
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response("Internal server error", 500)
    )
