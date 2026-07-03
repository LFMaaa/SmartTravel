FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（aiomysql 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common /app/common
COPY review-service /app/review-service

WORKDIR /app/review-service
ENV PYTHONPATH=/app

EXPOSE 8007
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8007"]
