FROM python:3.11-slim


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


EXPOSE 8080


CMD exec gunicorn --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    lmb_freight.wsgi:application