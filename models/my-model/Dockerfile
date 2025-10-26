# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model code
COPY src ./src
COPY configs ./configs

# Set default environment variables
ENV MODE="inference"
ENV CONFIG_PATH="configs/dev.yaml"
ENV AWS_DEFAULT_REGION="us-east-1"

# Entrypoint: decides train, inference or validate based on MODE
ENTRYPOINT ["python", "src/entrypoint.py"]
