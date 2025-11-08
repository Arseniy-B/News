from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from src.use_cases.exceptions import UserNotAuthorized


async def handler(request: Request, exc: UserNotAuthorized) -> Response:
    return JSONResponse(
        {"details": "premission denied"}, status_code=status.HTTP_401_UNAUTHORIZED
    )
