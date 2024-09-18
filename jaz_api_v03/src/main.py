import logging
import os

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import routes as auth
from .db.session import async_session_local
from .external_apis.safaricom import routes as safaricom
from .gwt_poc import routes as gwt_poc
from .html_poc import routes as html_poc
from .masters import models as master_models
from .masters import routes as masters
from .ping import routes as ping
from .premia import routes as policies
from .quotes import routes as quotes

# xtype: ignore

# Setup basic logging configuration
logging.basicConfig(filename="middleware_errors.log", level=logging.ERROR, format='%(asctime)s %(message)s')


# Custom middleware class to catch all exceptions globally
class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Call the next middleware or endpoint in the request chain
            response = await call_next(request)
            return response
        except Exception as exc:
            # Log the exception
            logging.error(f"Unhandled exception: {exc}")

            # Optionally save to a database here (pseudo-code):
            # db_session.add(LogEntry(error_message=str(exc), path=request.url.path))
            # db_session.commit()
            error_log = master_models.ErrorLog(
                path=str(request.url.path), error_log=str(exc)
            )
            async_db = async_session_local()
            async_db.add(error_log)
            await async_db.commit()
            await async_db.refresh(error_log)
            # await self.log_error(error_log)

            # Return a custom error response
            return JSONResponse(
                status_code=500,
                content={"message": "An internal server error occurred. Please try again later."},
            )


def create_application() -> FastAPI:
    fastapi_app = FastAPI(
        title="Jazk API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    # Add middleware
    # fastapi_app.add_middleware(ExceptionHandlingMiddleware)

    fastapi_app.include_router(ping.router, prefix="/ping", tags=["ping"])
    fastapi_app.include_router(auth.router, prefix="/auth", tags=["auth"])
    fastapi_app.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
    fastapi_app.include_router(policies.router, prefix="/policies", tags=["policies"])
    fastapi_app.include_router(safaricom.router, prefix="/extern", tags=["external_apis"])

    fastapi_app.include_router(masters.router, prefix="/masters", tags=["masters"])
    fastapi_app.include_router(html_poc.router, prefix="/portalx", tags=["portal"])
    fastapi_app.include_router(gwt_poc.router, tags=["stockwatcher"])

    # fastapi_app.mount("/", fastapi_app)
    path_str = os.path.dirname(os.path.realpath(__file__))
    fastapi_app.mount('/static', StaticFiles(directory=f"{path_str}/html_poc/static"), name='static')
    fastapi_app.mount('/gwt_static', StaticFiles(directory=f"{path_str}/gwt_poc/stockwatcher"), name='gwt_static')
    # fastapi_app.mount("/static", StaticFiles(directory="/usr/src/app/src/html_poc/static"), name="static")

    return fastapi_app


app = create_application()


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # print(exc.errors()[0])
    err = jsonable_encoder(exc.errors())
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": err})


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
