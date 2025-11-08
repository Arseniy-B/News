from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def handler(request: Request, exc: RequestValidationError) -> Response:
    errors = exc.errors()
    formatted = []
    for error in errors:
        formatted.append(error["msg"])
    return JSONResponse(
        {"detail": "; ".join(formatted)},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
