from fastapi import FastAPI
from src.drivers.routers.news import router


app = FastAPI()
app.include_router(router)

