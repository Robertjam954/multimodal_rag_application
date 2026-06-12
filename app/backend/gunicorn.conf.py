"""Gunicorn config. Uses our custom uvloop+uvicorn worker for Quart."""
import os

bind = f"0.0.0.0:{os.getenv('PORT', '50505')}"
workers = int(os.getenv("WEB_CONCURRENCY", "2"))
worker_class = "custom_uvicorn_worker.UvicornUvloopWorker"
keepalive = int(os.getenv("KEEPALIVE", "65"))
timeout = int(os.getenv("WORKER_TIMEOUT", "300"))
graceful_timeout = 30
loglevel = os.getenv("LOG_LEVEL", "info").lower()
accesslog = "-"
errorlog = "-"
