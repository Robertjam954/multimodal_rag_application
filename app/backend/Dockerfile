FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps for pillow, libmagic, audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libmagic1 ffmpeg curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY app/backend/requirements.txt /tmp/requirements.txt
COPY app/backend/requirements.in /tmp/requirements.in
RUN pip install --no-cache-dir -r /tmp/requirements.in

COPY app/backend /app
COPY app/frontend/build /app/static

ENV PORT=50505
EXPOSE 50505

CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
