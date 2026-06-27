FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（aiomysql 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common /app/common
COPY user-service /app/user-service

WORKDIR /app/user-service
ENV PYTHONPATH=/app

EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
