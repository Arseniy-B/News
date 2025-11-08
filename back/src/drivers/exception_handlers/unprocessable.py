from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def handler(request: Request, exc: RequestValidationError) -> Response:
    errors = exc.errors()
    formatted = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        msg = error["msg"]
        formatted.append(f"error in field a {field}, {msg.lower()}")
    return JSONResponse(
        {"detail": "; ".join(formatted)},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
