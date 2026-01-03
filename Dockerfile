FROM python:3.10.16-slim

WORKDIR /api
COPY . /api

ARG _GITHUBTOKEN

# Install system dependencies including LaTeX for PDF generation
RUN apt update -y \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt install -y build-essential gcc libpq-dev ffmpeg libsm6 libxext6 libzbar0 python3-dev \
    && apt-get install -y texlive-latex-base texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt 

EXPOSE 8080

# Use gunicorn for production instead of runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "api_genai_reaseguros.wsgi:application"]
