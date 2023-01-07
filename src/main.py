from fastapi import FastAPI
from src.settings.settings import load_settings

app = FastAPI()


@app.get("/")
async def main_route():
    return {"message": "Hello, World!"}


@app.on_event("startup")
async def startup():
    await load_settings()
