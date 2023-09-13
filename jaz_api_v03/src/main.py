from fastapi import FastAPI

from .ping import ping  

# xtype: ignore

def create_application() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(ping.router)
    return fastapi_app

app = create_application()
