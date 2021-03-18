"Provide non-CDN-dependent Swagger & Redoc pages to FastAPI"
from pathlib import Path
from typing import Any, TYPE_CHECKING
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

if TYPE_CHECKING:
    from fastapi import Response

_STATIC_PATH = Path(__file__).parent / "static"


def FastAPIOffline(*args: Any, **kwargs: Any) -> FastAPI:
    "Return a FastAPI obj that doesn't rely on CDN for the documentation page"
    # Disable the normal doc & redoc pages
    kwargs["docs_url"] = None
    kwargs["redoc_url"] = None

    # Create the FastAPI object
    app = FastAPI(*args, **kwargs)

    # This mostly just keeps mypy happy
    assert isinstance(app.openapi_url, str)
    assert isinstance(app.swagger_ui_oauth2_redirect_url, str)
    openapi_url = app.openapi_url
    swagger_ui_oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url

    # Set up static file mount
    app.mount(
        "/static-offline-docs",
        StaticFiles(directory=_STATIC_PATH.as_posix()),
        name="static-offline-docs",
    )

    # Define the doc and redoc pages, pointing at the right files
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> "Response":
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static-offline-docs/swagger-ui-bundle.js",
            swagger_css_url="/static-offline-docs/swagger-ui.css",
        )

    @app.get(swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect() -> "Response":
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html() -> "Response":
        return get_redoc_html(
            openapi_url=openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static-offline-docs/redoc.standalone.js",
        )

    # Return the FastAPI object
    return app
