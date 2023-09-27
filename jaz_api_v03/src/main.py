from fastapi import FastAPI

from .auth import routes as auth
from .ping import routes as ping
from .quotes import routes as quotes

# xtype: ignore


def create_application() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(ping.router, prefix="/ping", tags=["ping"])
    fastapi_app.include_router(auth.router, prefix="/auth", tags=["auth"])
    fastapi_app.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
    return fastapi_app


app = create_application()
