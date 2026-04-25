# ── Build stage ────────────────────────────────────────
FROM python:3.10-slim AS base

WORKDIR /app

# Install dependencies first (layer-caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# ── Runtime ────────────────────────────────────────────
EXPOSE 5000

ENV FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
