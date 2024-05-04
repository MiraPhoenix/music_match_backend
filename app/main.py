from fastapi import FastAPI
from api.handlers import router

app = FastAPI()

app.include_router(router)