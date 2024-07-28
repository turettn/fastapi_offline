"""Provide non-CDN-dependent Swagger & Redoc pages to FastAPI"""

from .core import FastAPIOffline

__all__ = [
    "FastAPIOffline",
]
