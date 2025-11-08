from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from src.use_cases.exceptions import ClienValidationError


async def handler(request: Request, exc: ClienValidationError) -> Response:
    return JSONResponse(
        {"detail": str(exc)}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )
