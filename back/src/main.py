from fastapi import FastAPI, Depends
from src.drivers.routers.news import router as news_router
from src.drivers.routers.users import router as users_router


app = FastAPI()

app.include_router(news_router)
app.include_router(users_router)

