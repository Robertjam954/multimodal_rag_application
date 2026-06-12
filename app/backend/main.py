"""Gunicorn / Quart entry. `quart --app main:app run` or `gunicorn main:app`."""
import asyncio
import logging
import os

from app import create_app
from load_azd_env import load_azd_env

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

load_azd_env()
app = asyncio.run(create_app())
