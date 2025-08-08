# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Install system dependencies (Java for PySpark, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set workdir
WORKDIR /app

# Install Python dependencies first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn[standard] pytest flake8

# Copy project files
COPY . /app

# Create necessary directories
RUN mkdir -p /app/commodity_platform /app/commodity_platform/models /app/commodity_platform/data /app/output

# Expose API and Dashboard ports
EXPOSE 8000 8501

# Default command runs API; dashboard can be launched via docker-compose
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]