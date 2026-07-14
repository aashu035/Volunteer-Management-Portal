# ===========================
# Build Stage
# ===========================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ===========================
# Development Stage
# ===========================
FROM python:3.11-slim AS development

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ===========================
# Production Stage
# ===========================
FROM python:3.11-slim AS production

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --no-create-home appuser

COPY --from=builder /install /usr/local

ENV PYTHONPATH=/app

COPY . .

RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

USER appuser

EXPOSE 8000

CMD ["./start.sh"]
