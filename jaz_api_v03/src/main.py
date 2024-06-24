from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .auth import routes as auth
from .ping import routes as ping
from .premia import routes as policies
from .quotes import routes as quotes

# xtype: ignore


def create_application() -> FastAPI:
    fastapi_app = FastAPI(
        title="Jazk API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    fastapi_app.include_router(ping.router, prefix="/ping", tags=["ping"])
    fastapi_app.include_router(auth.router, prefix="/auth", tags=["auth"])
    fastapi_app.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
    fastapi_app.include_router(policies.router, prefix="/policies", tags=["policies"])
    return fastapi_app


app = create_application()


@app.get("/jazk_docs", include_in_schema=False)
async def get_swagger_documentation():  # type: ignore
    return get_swagger_ui_html(
        openapi_url="/jazk_openapi.json", title="docs"
    )  # noqa: F821 # type: ignore


@app.get("/jazk_redoc", include_in_schema=False)
async def get_redoc_documentation():  # type: ignore
    return get_redoc_html(openapi_url="/jazk_openapi.json", title="docs")


@app.get("/jazk_openapi.json", include_in_schema=False)
async def openapi():  # type: ignore
    # return get_openapi(title=app.title, version=app.version, routes=app.routes)
    return get_openapi(title="Jazk APIx", version="0.1.0", routes=app.routes)
