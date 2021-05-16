"Check the default FastAPI package to confirm our consts"
import inspect

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from fastapi_offline.consts import *


def test_swagger():
    params = inspect.signature(get_swagger_ui_html).parameters
    assert params["swagger_js_url"].default == SWAGGER_JS
    assert params["swagger_css_url"].default == SWAGGER_CSS
    assert params["swagger_favicon_url"].default == FAVICON


def test_redoc():
    params = inspect.signature(get_redoc_html).parameters
    assert params["redoc_js_url"].default == REDOC_JS
    assert params["redoc_favicon_url"].default == FAVICON
