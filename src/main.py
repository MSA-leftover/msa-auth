from fastapi import FastAPI
from .settings import load_settings
from .routes import routers


def create_app():
    """FastAPI 앱 생성

    Returns:
        _type_: FastAPI
    """
    app = FastAPI()

    for router in routers:
        app.include_router(router)

    return app


app = create_app()


@app.on_event("startup")
async def startup():
    await load_settings()
