FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（aiomysql 需要 gcc）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common /app/common
COPY payment-service /app/payment-service

WORKDIR /app/payment-service
ENV PYTHONPATH=/app

EXPOSE 8004
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
