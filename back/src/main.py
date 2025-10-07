from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.drivers.routers.news import router as news_router
from src.drivers.routers.users import router as users_router

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app = FastAPI()

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("aaa")
