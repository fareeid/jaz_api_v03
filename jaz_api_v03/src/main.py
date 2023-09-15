from fastapi import FastAPI

from .ping import routes

# xtype: ignore


def create_application() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(routes.router)
    return fastapi_app


app = create_application()
