from fastapi import FastAPI

from .auth import routes as auth
from .ping import routes as ping

# xtype: ignore


def create_application() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(ping.router, prefix="/ping", tags=["ping"])
    fastapi_app.include_router(auth.router, prefix="/auth", tags=["auth"])
    return fastapi_app


app = create_application()
