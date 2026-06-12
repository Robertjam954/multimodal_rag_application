"""Uvicorn worker with uvloop for Gunicorn. Mirrors azure-search-openai-demo."""
from uvicorn.workers import UvicornWorker


class UvicornUvloopWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools", "lifespan": "off"}
