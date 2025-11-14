from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.drivers.exception_handlers import unauthorized, unprocessable, validation
from src.drivers.routers.auth import router as auth_router
from src.drivers.routers.news import router as news_router
from src.drivers.routers.users import router as users_router
from src.logging_config import setup_logging
from src.use_cases.exceptions import ClienValidationError, UserNotAuthorized


setup_logging()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://178.72.150.69:5173",
]


app = FastAPI(
    exception_handlers={
        RequestValidationError: unprocessable.handler,
        # ClienValidationError: validation.handler,
        UserNotAuthorized: unauthorized.handler,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)
app.include_router(news_router)
app.include_router(users_router)
app.include_router(auth_router)
