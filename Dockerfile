FROM python:3.10.16-slim

WORKDIR /api
COPY . /api

ARG _GITHUBTOKEN

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gcc \
    libpq-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libzbar0 \
    python3-dev \
    libcairo2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Run from the folder where manage.py is
WORKDIR /api/api_genai_reaseguros

EXPOSE 8080

# Use gunicorn for production instead of runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "300", "api_genai_reaseguros.wsgi:application"]
